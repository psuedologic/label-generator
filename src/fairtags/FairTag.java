/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package fairtags;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.URL;
import javafx.application.Application;
import javafx.beans.Observable;
import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.value.ChangeListener;
import javafx.collections.FXCollections;
import javafx.collections.ObservableArray;
import javafx.collections.ObservableList;
import javafx.fxml.FXMLLoader;
import javafx.print.PrinterJob;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.stage.FileChooser;
import javafx.stage.FileChooser.ExtensionFilter;
import javafx.stage.Stage;
import javax.imageio.ImageIO;

/**
 *
 * @author Talon
 */
public class FairTag extends Application {
    
    //Default value
    private static final double DEFAULT_PPI = 72;
    private static final double[] DEFAULT_PAGE_SIZE = {8.5, 11};
    private static final int[] GRID = {2, 5};
    private static final int[] TILE_SIZE = {4, 2};
    private static final double[] INITIAL_PAGE_SIZE = {700, 900};
    
    private static ObservableList<Painting> paintings = FXCollections.observableArrayList();
    private static SimpleDoubleProperty PPI = new SimpleDoubleProperty( DEFAULT_PPI );
    private static SimpleIntegerProperty currentPage = new SimpleIntegerProperty( 0 );
    private static SimpleIntegerProperty totalPages = new SimpleIntegerProperty( 0 );
    private static ChangeListener<Number> stageSizeListener;
    private static ObservableList<Number> stageSize = FXCollections.observableArrayList(getPageSize()[0] * DEFAULT_PPI, getPageSize()[1] * DEFAULT_PPI);
    private static Stage stage;
    
    @Override
    public void start(Stage s) throws Exception {
        stage = s;
        //FXMLLoader fxmlLoader = new FXMLLoader();
        
        Parent root = FXMLLoader.load(getClass().getResource("/fxml/FairTag.fxml"));
        
        //Parent root = fxmlLoader.getRoot();
        
        Scene scene = new Scene(root);
        //scene.getStylesheets().clear();
        //scene.getStylesheets().add("file:///" + f.getAbsolutePath().replace("\\", "/"));
        scene.setFill( Color.LIGHTGREY );
        
        stage.setScene(scene);
        
        stage.setWidth(INITIAL_PAGE_SIZE[0]);
        stage.setHeight(INITIAL_PAGE_SIZE[1]);
        setTitle();
        
        stageSize.add(stage.getWidth());
        stageSize.add(stage.getHeight());
        
        stageSize.set(0, stage.getWidth());
        stageSize.set(1, stage.getHeight());
        stage.show();
        
        stageSizeListener = (observable, oldValue, newValue) -> {
            //System.out.println("Height: " + stage.getHeight() + " Width: " + stage.getWidth());
            stageSize.set(0, stage.getWidth());
            stageSize.set(1, stage.getHeight());
            //stage.show();
        };
        
        //stageSize.addListener((Observable obs) -> {System.out.println("test"); });

        stage.widthProperty().addListener(stageSizeListener);
        stage.heightProperty().addListener(stageSizeListener);
  
    }
    public static void saveFile() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Save File");
        fileChooser.setInitialFileName("FairTags.tag");
        //fileChooser.setSelectedExtensionFilter(new ExtensionFilter("Fair Tag data storage file.", ".tag", ".test"));
        
        File file = fileChooser.showSaveDialog(stage);
        if (file != null) {
            try {
                PrintWriter pw = new PrintWriter(file);
                StringBuilder sb = new StringBuilder();
                
                for (Painting painting : paintings) {
                    
                    sb.append(painting.getName());
                    sb.append("†");
                    sb.append(painting.getArtist());
                    sb.append("†");
                    sb.append(painting.getNameFontSize());
                    sb.append("†");
                    sb.append(painting.getArtistFontSize());
                    sb.append("†");
                    sb.append("\r\n");
                }
                pw.write(sb.toString());
                pw.close();
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    public static void loadFile() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Load File");
        fileChooser.setSelectedExtensionFilter(new ExtensionFilter("Fair Tag data storage file.", "*.tag"));
        
        File file = fileChooser.showOpenDialog(stage);
        int count = 0;
        if (file != null) {
            try {
                BufferedReader reader = new BufferedReader( new FileReader(file));
                paintings.clear();
                
                String nextLine;
                //Get the next line of the file
                while ((nextLine = reader.readLine()) != null) {
                    count++;
                    //if their is not enough data in the current line keep appending
                    while (nextLine.split("†", -1).length < 4) {
                        nextLine = nextLine + "\r\n" + reader.readLine();
                    }
                    
                    String[] line = nextLine.split("†");
                    
                    paintings.add(new Painting(line[0], line[1], 
                            Double.parseDouble(line[2]), Double.parseDouble(line[3])));
                }
                reader.close();
            }
            catch (Exception e) {
                e.printStackTrace();
            }
            totalPages.set(count / 10);
            setCurrentPage(1);
        }
    }
    public static void addBlankPage() {
        totalPages.set(getTotalPagesValue() + 1);
        
        for (int i = 0; i < GRID[0] * GRID[1]; i++) {
            paintings.add(new Painting());
        }
        setCurrentPage(totalPages.get());
    }
    public static void deletePage() {
        int pages = getTotalPagesValue();
        paintings.remove(pages * 10 - 10, pages * 10 - 1);
        
        totalPages.set(pages - 1);
        
        setCurrentPage(getTotalPagesValue());
    }
    private static void initializeNewPaintings() {
        for (int i = 0; i < GRID[0] * GRID[1]; i++) {
            paintings.add(new Painting());
        }
    }
    public static void clearPaintings() {
        paintings.clear();
    }
    public static PrinterJob loadPrinterSettings() {
        PrinterJob job = PrinterJob.createPrinterJob();
        //job.showPageSetupDialog(stage);
        job.showPrintDialog(stage);
        return job;
    }
    public static void setCurrentPage(int index) {
        currentPage.set(index);
        setTitle();
    }
    public static ObservableList<Number> getStageSize() {
        return stageSize;
    }
    public static SimpleIntegerProperty getCurrentPage() {
        return currentPage;
    }
    public static int getCurrentPageValue() {
        return currentPage.get();
    }
    
    public static int getTotalPagesValue() {
        return totalPages.get();
    }
    public static void setTotalPages(int pages) {
        totalPages.set(pages);
    }
    public static void setTitle() {
        if (getCurrentPageValue() == 0) {
            stage.setTitle("Fair Tag Creator - Select 'new' or 'load' to begin");
        }
        else {
            stage.setTitle("Fair Tag Creator - Page " + currentPage.getValue().toString() + " of " + totalPages.getValue().toString());
        }
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        launch(args);
    }
    public static Painting getPainting(int index) {
        return paintings.get(index);
    }

    public static double[] getPageSize() {
        return DEFAULT_PAGE_SIZE;
    }

    public static int[] getGrid() {
        return GRID;
    }

    public static int[] getTileSize() {
        return TILE_SIZE;
    }

    public static double getPPI() {
        return PPI.get();
    }

    public static void setPPI(double aPPI) {
        PPI.set(aPPI);
    }
    
}
