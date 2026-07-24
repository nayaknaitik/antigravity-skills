package main

import (
	"context"
	"errors"
	"fmt"
	"log/slog"
	"os"
	"os/signal"
	"sync"
	"sync/atomic"
	"syscall"
	"time"
)

type Side string

const (
	SideBuy  Side = "BUY"
	SideSell Side = "SELL"
)

type Order struct {
	ID        string
	AccountID string
	Symbol    string
	Side      Side
	Price     float64
	Quantity  float64
	CreatedAt time.Time
}

type TradingEngine struct {
	processedCount int64
	logger         *slog.Logger
}

func NewTradingEngine(logger *slog.Logger) *TradingEngine {
	return &TradingEngine{logger: logger}
}

func (e *TradingEngine) ProcessOrders(ctx context.Context, workers int, orders <-chan Order, results chan<- string) {
	var wg sync.WaitGroup
	for i := 0; i < workers; i++ {
		wg.Add(1)
		workerID := i + 1
		go func(id int) {
			defer wg.Done()
			for {
				select {
				case <-ctx.Done():
					e.logger.Info("worker stopping via context cancellation", "worker_id", id)
					return
				case order, ok := <-orders:
					if !ok {
						return
					}
					atomic.AddInt64(&e.processedCount, 1)
					msg := fmt.Sprintf("Worker %d executed order %s [%s %f %s @ %f]", id, order.ID, order.Side, order.Quantity, order.Symbol, order.Price)
					results <- msg
				}
			}
		}(workerID)
	}
	wg.Wait()
}

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
	slog.SetDefault(logger)

	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, syscall.SIGINT)
	defer stop()

	engine := NewTradingEngine(logger)
	ordersChan := make(chan Order, 100)
	resultsChan := make(chan string, 100)

	// Launch worker pool
	go engine.ProcessOrders(ctx, 4, ordersChan, resultsChan)

	// Results printer goroutine
	go func() {
		for res := range resultsChan {
			logger.Info("trade execution result", "detail", res)
		}
	}()

	// Feed test orders
	for i := 1; i <= 10; i++ {
		ordersChan <- Order{
			ID:        fmt.Sprintf("ORD-%04d", i),
			AccountID: "ACC-9912",
			Symbol:    "AAPL",
			Side:      SideBuy,
			Price:     185.50,
			Quantity:  100,
			CreatedAt: time.Now(),
		}
	}
	close(ordersChan)

	<-ctx.Done()
	logger.Info("trading engine shut down cleanly", "total_processed", atomic.LoadInt64(&engine.processedCount))
}
