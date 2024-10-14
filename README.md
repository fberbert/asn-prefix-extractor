# ASN Prefix Extractor

This script extracts customer ASNs that have a specific provider ASN from the [Radar Qrator](https://radar.qrator.net) website. The goal is to find customers that have only the specified provider as their active provider and at least one active IPv4 prefix.

## Features

- Scrapes data from the Radar Qrator website to find customer ASNs of a given provider ASN.
- Checks if each customer ASN has only one active provider and that it matches the specified provider ASN.
- Extracts the active IPv4 prefixes for each qualifying customer ASN.
- Stores the results in a text file, organized by ASN number, ASN name, and the corresponding IPv4 prefixes.

## Requirements

- Python 3.x
- Selenium
- WebDriver Manager

## Installation

Install the required dependencies with:

```bash
pip install selenium webdriver-manager
```

## Usage

1. **Edit the Script:**
   - Set the `provider_asn` variable in the script to the ASN of the provider whose customers you want to analyze.
   - Optionally, change the `output_file` variable if you want to output the results to a different file.

2. **Run the Script:**

   After setting the required variables, you can run the script:

   ```bash
   python asn_prefix_extractor.py
   ```

3. **Output:**

   The script generates a text file (by default `output.txt`) containing the ASN name, ASN number, and the list of active IPv4 prefixes for each customer that meets the criteria.

   Example output:
   ```
   ASN Name: Example ASN
   ASN Number: 12345
   IPv4 Prefixes:
   192.168.0.0/24
   203.0.113.0/24
   ```

## Code Overview

- **provider_asn**: The ASN of the provider whose customers are to be analyzed.
- **output_file**: The name of the output file (default: `output.txt`).
- The script navigates to the Radar Qrator website, retrieves a list of customer ASNs for the given provider, and for each customer, checks if they have only one active provider (the specified provider ASN). If they meet this criterion, the script fetches their active IPv4 prefixes.
- Only customers with at least one active IPv4 prefix are added to the output file.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
