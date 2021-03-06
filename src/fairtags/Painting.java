package fairtags;

import javafx.beans.property.SimpleBooleanProperty;
import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;

/**
 * @author Talon
 */
public class Painting {
    private final SimpleStringProperty name = new SimpleStringProperty("");
    private final SimpleStringProperty artist = new SimpleStringProperty("");
    private final SimpleDoubleProperty nameFontSize = new SimpleDoubleProperty(0);
    private final SimpleDoubleProperty artistFontSize = new SimpleDoubleProperty(0);
    private final SimpleBooleanProperty isAdult = new SimpleBooleanProperty(true);
    
    public Painting() {
        this("","");
    }
    public Painting(boolean isAdult) {
        this("","", isAdult);
    }
    public Painting(String name, String author) {
        this(name, author, 24.0, 16.0, true);
    }
    public Painting(String name, String author, boolean isAdult) {
        this(name, author, 24.0, 16.0, isAdult);
    }
    public Painting(String name, String author, double nameFontSize, double authorFontSize, boolean isAdult) {
        this.setName(name);
        this.setArtist(author);
        this.setNameFontSize(nameFontSize);
        this.setArtistFontSize(authorFontSize);
        this.setIsAdult(isAdult);
    }
    public final void setName(String name) {
        this.name.set(name);
    }
    public final String getName() {
        return name.get();
    }
    public final void setArtist(String author) {
        this.artist.set(author);
    }
    public final String getArtist() {
        return artist.get();
    }
    public final void setNameFontSize(double nameFontSize) {
        this.nameFontSize.set(nameFontSize);
    }
    public final Double getNameFontSize() {
        return nameFontSize.get();
    }
    public final void setArtistFontSize(double authorFontSize) {
        this.artistFontSize.set(authorFontSize);
    }
    public final Double getArtistFontSize() {
        return artistFontSize.get();
    }
    public final void setIsAdult(boolean isAdult) {
        this.isAdult.set(isAdult);
    }
    public final Boolean getIsAdult() {
        return isAdult.get();
    }
}
