import java.sql.*;
import java.util.*;


/*
    IN2090 - H2018
    Oblig 6 
    uio-brukernavn: peterrl

*/

public class TimelisteDb {
    private Connection connection;

    public TimelisteDb(Connection connection) {
        this.connection = connection;
    }



    public void printTimelister() throws SQLException {
        
            // Skap et statement objekt.
            Statement statement = connection.createStatement();

            // Spørring som skal kjøres.
            String selectQuery = "SELECT * FROM tliste";

            // Kjør spørring og lagre resultatene.
            ResultSet results = statement.executeQuery(selectQuery);

            System.out.println("Timelister:");
            System.out.println("--------------------------");
            while(results.next()){

                // Hent ut Dataen.
                int timelistenr = results.getInt("timelistenr");
                String status = results.getString("status");
                String beskrivelse = results.getString("beskrivelse");

                String lastSpace = ""; 
                for(;lastSpace.length() < 16 - status.length(); lastSpace+= " ");

                // Skriv ut print av timeliste med data fra spørringen.
                System.out.println("nr: "+ timelistenr + "  status: " + status + lastSpace+ " beskrivelse:    " + beskrivelse);
            }
    }






    public void printTimelistelinjer(int timelisteNr) throws SQLException {

        // 'Prepared' Select spørring med ledig plass for timelistenr.
        String selectQuery = "SELECT linjenr, timeantall, beskrivelse, kumulativt_timeantall FROM tlistelinje where timelistenr = ?";
        PreparedStatement prepStatement = connection.prepareStatement(selectQuery);
        prepStatement.setInt(1,timelisteNr); // Faktisk sette timelistenr i den 'forberedte' spørringen.
            

        // Kjør spørring og hent resultat.
        ResultSet results = prepStatement.executeQuery();

        System.out.println("---------------------------------");
        
        // Itererer gjennom resultatene
        while(results.next()){

            // Og lagerer dataen i passende variabler
            int linjenr                  = results.getInt("linjenr");
            int timeantall               = results.getInt("timeantall");
            String beskrivelse           = results.getString("beskrivelse");
            int kumulativt_timeantall    = results.getInt("kumulativt_timeantall");

            // Litt formaterings hjelp.
            String lastSpace = ""; 
            for(;lastSpace.length() < 32 - beskrivelse.length(); lastSpace+= " ");

            // Print ut timelistelinjen med dataen fra spørringen.
            System.out.println("linjenr:    "+ linjenr + "  timeantall: " + timeantall + "  beskrivelse:    " + beskrivelse + lastSpace + "kumulativt_timeantall:  " + kumulativt_timeantall);
        }

    }





    public double medianTimeantall(int timelisteNr) throws SQLException {

        // 'Prepared' select spørring med stigende sortering gjennom ORDER BY.
        String selectQuery = "SELECT timeantall FROM tlistelinje where timelistenr = ? ORDER BY timeantall ASC";

        PreparedStatement prepStatement = connection.prepareStatement(selectQuery);
        prepStatement.setInt(1,timelisteNr); // sett timelistenr i spørringen.
        
        // kjør spørring.
        ResultSet results = prepStatement.executeQuery();

        // lagre alle timeAntallene i spørringen i en liste.
        ArrayList<Integer> timeAntallListe = new ArrayList<>();

        // Iterer over resultatene og legg de til i listen.
        while(results.next()){
                timeAntallListe.add(results.getInt("timeantall"));
        }

        // Bruker den hjelpsomme median metoden til å finen medianen med den pres-sorterte listen som argument.
        return median(timeAntallListe);
    }







    public void settInnTimelistelinje(int timelisteNr, int antallTimer, String beskrivelse) throws SQLException {

        // Insert 'spørring' for ny timelistelinje som inneholder subspørring som automatisk setter riktig linjeNr. 
        String insertQuery = "INSERT INTO tlistelinje (linjenr, timelistenr, timeantall, beskrivelse ) VALUES ( (select MAX(linjenr) from tlistelinje WHERE timelistenr = ? ) + 1 , ? , ? , ? )";
        PreparedStatement prepStatement = connection.prepareStatement(insertQuery);

        // Sett korrekt data inn i spørringssetningen.
        prepStatement.setInt(1, timelisteNr);
        prepStatement.setInt(2, timelisteNr);
        prepStatement.setInt(3, antallTimer);
        prepStatement.setString(4, beskrivelse);

        // Utfør spørring.
        prepStatement.executeUpdate();


    }




    

    public void regnUtKumulativtTimeantall(int timelisteNr) throws SQLException {
   
         // Forbered Selectspørring for å finne de riktige timelistelinjene.
         String selectQuery = "SELECT timeantall, linjeNr FROM tlistelinje WHERE timelistenr = ?";
         PreparedStatement prepStatement = connection.prepareStatement(selectQuery);
         prepStatement.setInt(1,timelisteNr);

         // Utfør spørring og lagre resultatet.
         ResultSet results = prepStatement.executeQuery();

         
         // Forbered oppdaterings-spørring
         String updateQuery = "UPDATE tlistelinje SET kumulativt_timeantall = ? WHERE timelistenr = ? AND linjenr = ?";

         // Variabel som holder det kumulative_antallet etterhvert som det stiger.
         int kumulativt_antall = 0; 
         while(results.next()){
            
            kumulativt_antall += results.getInt("timeantall");        // Inkrementér det kumulative_antallet

            prepStatement = connection.prepareStatement(updateQuery); // Resirkulerer den forrige PreparedStatement pekeren.
            prepStatement.setInt(1, kumulativt_antall);               // Sett antallet på UPDATE-spørringen
            prepStatement.setInt(2, timelisteNr);                     // Sett timelisteNr for UPDATE-spørringen.
            prepStatement.setInt(3, results.getInt("linjenr"));       // Sett linjenr på UPDATE-spørringen 
            prepStatement.executeUpdate();                            // Utfør UPDATE-spørringen for den gjeldende linjen.

         }
    } 



    /**
     * Hjelpemetode som regner ut medianverdien i en SORTERT liste. Kan slettes om du ikke har bruk for den.
     * @param list Tar inn en sortert liste av integers (f.eks. ArrayList, LinkedList osv)
     * @return medianverdien til denne listen
     */
    private double median(List<Integer> list) {
        int length = list.size();
        if (length % 2 == 0) {
            return (list.get(length / 2) + list.get(length / 2 - 1)) / 2.0;
        } else {
            return list.get((length - 1) / 2);
        }
    }
}
