package com.company.payment;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class FlawedPaymentService {

    // HARDCODED SECRET
    private static final String API_SECRET = "sk_live_99182381283912831293";

    // FLOATING POINT MONEY
    public double processPayment(double amount, String user) {
        try {
            // UNCLOSED CONNECTION & SQL INJECTION
            Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5432/mydb", "user", "pass");
            Statement stmt = conn.createStatement();
            stmt.executeUpdate("SELECT * FROM users WHERE name = '" + user + "'");
            
            // SYSTEM OUT PRINT
            System.out.println("Processed payment of " + amount);
            return amount * 0.95;
        } catch (Exception e) {
            // SWALLOWED EXCEPTION
            return 0.0;
        }
    }
}
