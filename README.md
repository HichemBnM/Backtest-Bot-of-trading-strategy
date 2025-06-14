# Crypto Trading Bot Backtest

This project implements a backtesting strategy for cryptocurrency trading using technical indicators such as EMA, MACD, and ATR. The bot evaluates entry and exit signals based on a score system and calculates performance metrics.

## Features

- **Technical Indicators**: Calculates EMA, MACD Histogram, and ATR.
- **Score-Based Entry Signal**: Generates trading signals based on indicator trends.
- **Backtesting Logic**: Simulates trades with entry, exit, and stop-loss conditions.
- **Performance Metrics**: Summarizes results with win rate, average P/L, CAGR, and more.
- **Excel Integration**: Reads input data from `btc_data.xlsx` and saves trade results to `trades.xlsx`.

## Project Structure

```
backtest.docx
backtest.zip
bot.py
btc_data.xlsx
summary.xlsx
trades.xlsx
```

- `bot.py`: Main script for backtesting logic.
- `btc_data.xlsx`: Input data containing historical cryptocurrency prices.
- `trades.xlsx`: Output file containing trade results.
- `summary.xlsx`: Summary statistics (optional).
- `backtest.docx` and `backtest.zip`: Documentation and archived files.

## Requirements

- Python 3.x
- Libraries: `pandas`, `numpy`, `ta`, `openpyxl`

Install dependencies using:

```sh
pip install pandas numpy ta openpyxl
```

## Usage

1. Place the historical cryptocurrency data in `btc_data.xlsx`.
2. Run the script:

```sh
python bot.py
```

3. Check the generated `trades.xlsx` for trade results and summary statistics printed in the console.

## Output

- **Trade Results**: Saved in `trades.xlsx`.
- **Summary Statistics**: Displayed in the console.

## Example

Sample summary statistics:

```
Total Trades: 50
Win Rate: 0.60
Average P/L: 150.25
Total P/L: 7512.50
Average Win: 300.50
Average Loss: -200.75
Avg Days Held (Win): 5.2
Avg Days Held (Loss): 3.8
CAGR: 12.5%
Starting Bank: 50000
Ending Bank: 57512.50
```

## License

This project is licensed under the MIT License.

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## Author

Created by [Your Name].
