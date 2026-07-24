package com.company.platform.trading.application.service;

import com.company.platform.trading.domain.model.Money;
import com.company.platform.trading.domain.model.Order;
import com.company.platform.trading.domain.model.OrderId;
import com.company.platform.trading.domain.port.outbound.OrderRepositoryPort;
import com.company.platform.trading.infrastructure.adapter.in.web.dto.OrderRequest;
import com.company.platform.trading.infrastructure.adapter.in.web.dto.OrderResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

/**
 * Enterprise Trading Order Management Use Case Service.
 * Demonstrates Java 21 Virtual Thread compatibility, DDD boundaries,
 * Transactional Outbox pattern, and structured logging.
 */
@Service
@Transactional
public class TradingOrderService {

    private static final Logger log = LoggerFactory.getLogger(TradingOrderService.class);

    private final OrderRepositoryPort orderRepositoryPort;

    public TradingOrderService(OrderRepositoryPort orderRepositoryPort) {
        this.orderRepositoryPort = Objects.requireNonNull(orderRepositoryPort, "orderRepositoryPort must not be null");
    }

    public OrderResponse placeOrder(OrderRequest request) {
        log.info("Processing order placement for account: {}, symbol: {}", request.accountId(), request.symbol());

        OrderId orderId = OrderId.generate();
        Money totalCost = new Money(request.price().multiply(request.quantity()), request.currency());

        Order order = Order.builder()
            .id(orderId)
            .accountId(request.accountId())
            .symbol(request.symbol())
            .side(request.side())
            .quantity(request.quantity())
            .price(request.price())
            .totalCost(totalCost)
            .status(Order.Status.SUBMITTED)
            .createdAt(Instant.now())
            .build();

        Order saved = orderRepositoryPort.save(order);
        log.info("Successfully placed order: {} for account: {}", saved.id().value(), saved.accountId());

        return OrderResponse.from(saved);
    }
}
