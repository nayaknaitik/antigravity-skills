package com.company.payment;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.Objects;
import java.util.UUID;

@Service
@Transactional
public class ProductionPaymentService {

    private static final Logger log = LoggerFactory.getLogger(ProductionPaymentService.class);

    private final PaymentRepositoryPort repository;

    public ProductionPaymentService(PaymentRepositoryPort repository) {
        this.repository = Objects.requireNonNull(repository, "repository must not be null");
    }

    public PaymentResponse processPayment(UUID userId, BigDecimal amount, String currency) {
        log.info("Processing secure payment for user: {}, amount: {} {}", userId, amount, currency);

        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Payment amount must be positive");
        }

        Payment payment = Payment.create(userId, amount, currency);
        Payment saved = repository.save(payment);

        return PaymentResponse.from(saved);
    }
}
