package fairtags;

import java.net.URL;
import java.util.Optional;
import java.util.ResourceBundle;
import javafx.beans.Observable;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.event.ActionEvent;
import javafx.event.Event;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.print.PageLayout;
import javafx.print.PageOrientation;
import javafx.print.PageRange;
import javafx.print.Paper;
import javafx.print.Printer;
import javafx.print.PrinterJob;
import javafx.scene.control.Alert;
import javafx.scene.control.ButtonType;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.input.MouseEvent;
import javafx.scene.input.ScrollEvent;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.GridPane;
import javafx.scene.shape.Line;
import javafx.scene.text.Font;
import javafx.stage.Modality;

/**
  * @author Talon
 */
public class FairTagController implements Initializable {
    
    @FXML GridPane gridPane;
    @FXML TextArea textAreaName0;
    @FXML Label labelName0;
    @FXML TextField fontSize;
    @FXML Line border1;
    @FXML Line border2;
    private final SimpleIntegerProperty currentSelection = new SimpleIntegerProperty(-1);
    private AnchorPane currentPane;
    private TextArea textAreaName;
    private Label labelName;
    private TextArea textAreaArtist;
    private Label labelArtist;
    private String currentlyEditing = "";
    
    @FXML 
    private void selectName(MouseEvent event) {
        editText(event, 0);
    }
    @FXML
    private void zoom(ScrollEvent event) {
        double scale = gridPane.getScaleX();
        if (event.getDeltaY() > 0) {
            scale += .1;
        }
        else {
            scale -= .1;
        }
        gridPane.setScaleX(scale);
        gridPane.setScaleY(scale);
    }
    @FXML
    private void selectArtistName(MouseEvent event) {
        editText(event, 10);
    }
    private void editText(MouseEvent event, int offset) {
        if (getCurrentSelection() != -1) {
            clearTextSelection();
        }
        setCurrentSelection(event, offset);
        
        labelName.setVisible(false);
        textAreaName.setVisible(true);

        fontSize.setText("" + Math.round(labelName.getFont().getSize()));
    }
    
    @FXML
    private void changeFontSize(ActionEvent event) {
        TextField fontField = ((TextField) event.getSource());
        int fontSize = 0;
        
        try {
            fontSize = Integer.parseInt(fontField.getText());
            textAreaName.setFont(new Font("Arial", fontSize));
            labelName.setFont(new Font("Arial", fontSize));
        }
        catch (NumberFormatException e) {
            fontField.setText("" + textAreaName.getFont().getSize());
        }
        
    }
    
    @FXML
    private void clearTextSelection() {
        if (getCurrentSelection() != -1) {
            textAreaName.setVisible(false);
            labelName.setVisible(true);
            labelName.setText(textAreaName.getText());
            
            int index = (getCurrentSelection() % 10);
            
            Painting painting = FairTag.getPainting(index + (FairTag.getCurrentPageValue() - 1) * 10);
            if (getCurrentSelection() < 10) {
                painting.setName(textAreaName.getText());
                painting.setNameFontSize(textAreaName.getFont().getSize());
            }
            else {
                painting.setArtist(textAreaName.getText());
                painting.setArtistFontSize(textAreaName.getFont().getSize());
            }

            currentSelection.set(-1);
            fontSize.setText("");
            currentlyEditing = "";
        }
    }

    private void editText(AnchorPane pane) {
        
    }
    private void setCurrentSelection(Event event, int offset) {
        AnchorPane pane = (AnchorPane) ((Label) event.getSource()).getParent();
        currentSelection.set(pane.getParent().getChildrenUnmodifiable().indexOf(pane) + offset);
    }
    private int getCurrentSelection() {
        return currentSelection.get();
    }
    private void selectFields() {
        int selectedField = currentSelection.get();
        if (selectedField == -1) {
            currentPane = null;
            textAreaName = null;
            labelName = null;
            fontSize.setEditable(false);
        }
        else if(selectedField < 10) {
            currentPane = (AnchorPane) gridPane.getChildrenUnmodifiable().get(currentSelection.get());
            textAreaName = ((TextArea) (currentPane.getChildren().get(1)));
            labelName = (Label) currentPane.getChildren().get(2);
            fontSize.setEditable(true);
        }
        else if (selectedField < 20) {
            currentPane = (AnchorPane) gridPane.getChildrenUnmodifiable().get(currentSelection.get() - 10);
            textAreaName = ((TextArea) (currentPane.getChildren().get(3)));
            labelName = (Label) currentPane.getChildren().get(4);
            fontSize.setEditable(true);
        }
    }
    @FXML
    private void closeDocument() {
        if (FairTag.getTotalPagesValue() != 0) {
            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.initModality(Modality.NONE);

            alert.setTitle("Close document confirmation");
            alert.setHeaderText("Close document?");
            alert.setContentText("Are you sure you want to close document?");

            Optional<ButtonType> result = alert.showAndWait();
            if (result.isPresent() && result.get() == ButtonType.OK) {
                clearStage();
                FairTag.setCurrentPage(0);
                FairTag.setTotalPages(0);
                FairTag.clearPaintings();
            }
        }
    }
    
    private void clearStage() {
        gridPane.setVisible(false);
    }
    @FXML 
    private void loadNewDocument(ActionEvent event) {
        if (FairTag.getCurrentPageValue() == 0) {
            gridPane.setVisible(true);
            FairTag.addBlankPage();
            loadPage(1);
        }
    }
    @FXML
    private void loadNextPage(ActionEvent event) {
        clearTextSelection();
        if (FairTag.getCurrentPageValue() < FairTag.getTotalPagesValue()
                && FairTag.getCurrentPageValue() != 0) {
            FairTag.setCurrentPage(FairTag.getCurrentPageValue() + 1);
            loadPage(FairTag.getCurrentPageValue());
        }
        else if (FairTag.getCurrentPageValue() != 0) {
            FairTag.addBlankPage();
            loadPage( FairTag.getCurrentPageValue());
        }
    }
    @FXML
    private void loadPreviousPage(ActionEvent event) {
        clearTextSelection();
        if (FairTag.getCurrentPageValue() > 1) {
            FairTag.setCurrentPage(FairTag.getCurrentPageValue() - 1);
            loadPage(FairTag.getCurrentPageValue());
        }
    }
    @FXML
    private void deletePage(ActionEvent event) {
        if (FairTag.getCurrentPageValue() == FairTag.getTotalPagesValue()
                && (FairTag.getCurrentPageValue() != 0) 
                && (FairTag.getTotalPagesValue() != 1)){
            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.initModality(Modality.NONE);

            alert.setTitle("Delete page confirmation");
            alert.setHeaderText("Delete page?");
            alert.setContentText("Are you sure you want to delete this page?");

            Optional<ButtonType> result = alert.showAndWait();
            if (result.isPresent() && result.get() == ButtonType.OK) {
                FairTag.deletePage();
                loadPage(FairTag.getCurrentPageValue());
            }
        }
    }
    @FXML
    private void saveDocument(ActionEvent event) {
        if (FairTag.getCurrentPageValue() != 0) {
            FairTag.saveFile();
        }
    }
    @FXML
    private void loadDocument(ActionEvent event) {
        FairTag.loadFile();
        loadPage(1);
        gridPane.setVisible(true);
    }
    private void loadPage(int index) {
        index--;
        
        for (int i = 0; i < 10; i++) {
            currentPane = (AnchorPane) gridPane.getChildrenUnmodifiable().get(i);
            Painting painting = FairTag.getPainting(i + index * 10);
            
            TextArea text = ((TextArea) (currentPane.getChildren().get(1)));
            text.setText(painting.getName());
            text.setFont(Font.font ("Arial", painting.getNameFontSize()));
            
            Label name = (Label) currentPane.getChildren().get(2);
            name.setText(painting.getName());
            name.setFont(Font.font ("Arial", painting.getNameFontSize()));
            
            text = ((TextArea) (currentPane.getChildren().get(3)));
            text.setText(painting.getArtist());
            text.setFont(Font.font ("Arial", painting.getArtistFontSize()));
            
            name = (Label) currentPane.getChildren().get(4);
            name.setText(painting.getArtist());
            name.setFont(Font.font ("Arial", painting.getArtistFontSize()));
        }
    }
    @FXML
    private void print() {
        if (FairTag.getCurrentPageValue() != 0) {
            PrinterJob job = FairTag.loadPrinterSettings();
            PageRange[] range = job.getJobSettings().getPageRanges();
            
            int startPage = 1;
            int endPage = FairTag.getTotalPagesValue();
            
            if (range != null) {
                for (PageRange r : range) {
                    startPage = r.getStartPage();
                    endPage = Math.min(endPage, r.getEndPage());
                }
            }
            
            //Printer defaultPrinter = Printer.getDefaultPrinter();
            
            //job.setPrinter(defaultPrinter);
            Printer printer = job.getPrinter();
            PageLayout pageLayout = printer.createPageLayout(Paper.NA_LETTER, PageOrientation.PORTRAIT, 0,0,0,0 );

            int currentPage = FairTag.getCurrentPageValue();
            double x = gridPane.getLayoutX();
            double y = gridPane.getLayoutY();
            double scaleX = gridPane.getScaleX();
            double scaleY = gridPane.getScaleY();
            gridPane.setLayoutX(0);
            gridPane.setLayoutY(0);
            gridPane.setScaleX(1);
            gridPane.setScaleY(1);
            
            
            border1.setStartX(gridPane.getChildren().get(1).getLayoutX());
            border1.setEndX(gridPane.getChildren().get(1).getLayoutX());
            border1.setVisible(true);
            border2.setVisible(true);
           

            if (job != null) {
                System.out.println(startPage);
                System.out.println(endPage);
                for (int i=startPage; i<=endPage; i++) {
                    FairTag.setCurrentPage(i);
                    loadPage(i);
                    job.printPage(pageLayout, gridPane);
                }
                
                job.endJob();
            }
            
            FairTag.setCurrentPage(currentPage);
            loadPage(currentPage);
                    
            gridPane.setLayoutX(x);
            gridPane.setLayoutY(y);
            gridPane.setScaleX(scaleX);
            gridPane.setScaleY(scaleY);
            
            border1.setVisible(false);
            border2.setVisible(false);
        }
    }
    
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        clearStage();
        
        currentSelection.addListener((Observable o) -> {
            selectFields();
        });
        SimpleIntegerProperty currentPage = FairTag.getCurrentPage();
        
        FairTag.getStageSize().addListener((Observable o) -> {
           double pageSizeX = (FairTag.getPPI() * FairTag.getPageSize()[0]);
           double pageSizeY = (FairTag.getPPI() * FairTag.getPageSize()[1]);
           
           gridPane.setLayoutX( (FairTag.getStageSize().get(0).doubleValue() - pageSizeX) / 2 );
           gridPane.setLayoutY( (FairTag.getStageSize().get(1).doubleValue() - pageSizeY) / 2 );
           gridPane.centerShapeProperty().setValue(Boolean.TRUE);
        });
    }    
    
}
