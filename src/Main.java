import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class Main {
    public static void main(String[] args) {
        String url = "jdbc:sqlite:test.db";

        try (Connection conn = DriverManager.getConnection(url);
             Statement stmt = conn.createStatement()) {

            // create a table
            stmt.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)");

            // insert a row
            stmt.execute("INSERT INTO users (name) VALUES ('Joanna')");

            // query the table
            ResultSet rs = stmt.executeQuery("SELECT * FROM users");

            while (rs.next()) {
                System.out.println("User ID: " + rs.getInt("id") + ", Name: " + rs.getString("name"));
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
