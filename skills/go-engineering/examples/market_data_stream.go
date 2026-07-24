package main

import (
	"context"
	"fmt"
	"log/slog"
	"os"
	"time"
)

type Tick struct {
	Symbol    string
	Bid       float64
	Ask       float64
	Timestamp time.Time
}

type MarketDataStream struct {
	logger *slog.Logger
}

func NewMarketDataStream(logger *slog.Logger) *MarketDataStream {
	return &MarketDataStream{logger: logger}
}

func (s *MarketDataStream) StreamTicks(ctx context.Context, symbol string, out chan<- Tick) {
	ticker := time.NewTicker(100 * time.Millisecond)
	defer ticker.Stop()

	basePrice := 150.00
	count := 0

	for {
		select {
		case <-ctx.Done():
			s.logger.Info("stopping market data stream", "symbol", symbol)
			return
		case t := <-ticker.C:
			count++
			out <- Tick{
				Symbol:    symbol,
				Bid:       basePrice + float64(count)*0.05,
				Ask:       basePrice + float64(count)*0.05 + 0.02,
				Timestamp: t,
			}
			if count >= 5 {
				return
			}
		}
	}
}

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
	stream := NewMarketDataStream(logger)

	ticks := make(chan Tick, 10)
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	go func() {
		stream.StreamTicks(ctx, "MSFT", ticks)
		close(ticks)
	}()

	for tick := range ticks {
		fmt.Printf("[%s] Bid: %.2f | Ask: %.2f\n", tick.Symbol, tick.Bid, tick.Ask)
	}
}
