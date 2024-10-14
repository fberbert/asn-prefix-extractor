# ASN Prefix Extractor

This script extracts data from [Qrator Radar](https://radar.qrator.net/) for a specified provider ASN, listing all customer ASNs that have the provider as their only active upstream provider and have at least one active IPv4 prefix. The extracted data is saved in a CSV file.

## Features

- **Extracts customer ASNs** that are connected to a specific provider ASN.
- **Filters customers** who have only the specified provider as their active upstream.
- **Retrieves active IPv4 prefixes** of customers and stores them in the output file.
- Output data includes:
  - ASN Number
  - ASN Name
  - Customer URL
  - List of active IPv4 prefixes

## Prerequisites

- Python 3.x
- Selenium
- ChromeDriver (managed by `webdriver-manager`)

### Install dependencies

You can install the required dependencies using:

```bash
pip install selenium webdriver-manager
```

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/asn-prefix-extractor.git
   cd asn-prefix-extractor
   ```

2. Edit the script to set the provider ASN you wish to analyze. 

3. Run the script:

   ```bash
   python3 asn-prefix-extractor.py
   ```

4. The output will be saved in the specified CSV file (`output.csv` by default), containing the following columns:
   - ASN Number
   - ASN Name
   - Customer URL
   - List of IPv4 prefixes (if available)

## Configuration

The following variables can be set at the beginning of the script:
- `output_file`: The name of the CSV file where the results will be stored.
- `provider_asn`: The ASN of the provider you want to analyze (default is set to `28260`).

## Example Output

```csv
ASN Number,ASN Name,Customer URL,IPv4 Prefixes
12345,Example AS,https://radar.qrator.net/as/12345/connectivity/neighbors/providers,"192.0.2.0/24, 198.51.100.0/24"
...
```

## Headless Mode

By default, the script runs in headless mode, meaning it does not open a visible browser window. If you want to disable headless mode for debugging purposes, you can remove the following line in the script:

```python
chrome_options.add_argument("--headless")
```

## Troubleshooting

### Slow Loading Pages

If you encounter issues where pages take too long to load, try increasing the `time.sleep(10)` delay between requests. You may also want to monitor the page loading process manually by disabling headless mode.

### No Data in Output File

Ensure that the provider ASN has active customers and that Qrator Radar is up and running. If no customer ASNs meet the filter criteria, the output file may be empty.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Feel free to submit pull requests or open issues to improve the script.
