# apigw-colab-common

Shared **UI widgets** for Google Colab notebooks that work with the Kyriba API Gateway.

This library centralizes only:

- Admin client selection widget
- Platform selection widget (with search and “select all”)
- A helper to normalize / expand platform selections (`ALL`, `ALL PROD`, `ALL PROD AND SANDBOX`)

It is designed so that multiple Colab notebooks can use the same selection logic and stay in sync as the list of platforms evolves.

> **Note:** All HTTP / OAuth / API logic lives in your notebooks.  
> This repo is strictly for the **selection widgets** and their utilities.

---

## Table of contents

- [Why this exists](#why-this-exists)
- [What’s included](#whats-included)
- [Installing in Google Colab](#installing-in-google-colab)
    - [Option 1: Clone the repo in each Colab](#option-1-clone-the-repo-in-each-colab)
    - [Option 2: Use in a shared Google Drive folder](#option-2-use-in-a-shared-google-drive-folder)
- [Basic usage](#basic-usage)
    - [1. Create widgets](#1-create-widgets)
    - [2. Normalize platform selection](#2-normalize-platform-selection)
    - [3. Read admin client value](#3-read-admin-client-value)
- [API reference (high level)](#api-reference-high-level)
- [Updating the library](#updating-the-library)

---

## Why this exists

We had many separate Colab notebooks that all needed the same:

- “Select admin client” dropdown
- “Select platforms” widget with search and special values (`ALL`, `ALL PROD`, `ALL PROD AND SANDBOX`)
- Logic to expand those special values into concrete hostnames

Instead of copy-pasting that code into every notebook, this repo provides a single shared widget module that all Colabs can import. Update the logic once, and all notebooks benefit.

---

## What’s included

The main module is:

- `apigw_common.py`

Key features:

- **Admin client widget**
    - `create_admin_client_selector(default_value=...)`
    - Nicely styled dropdown with predefined admin client IDs
    - Helper: `get_admin_client_value(admin_widget, default=...)`

- **Platform selection widget**
    - `create_platform_selector()`
    - Multiselect list of platforms
    - Search box (filters list as you type)
    - “Select all visible platforms” checkbox
    - Special entries:
        - `ALL`
        - `ALL PROD`
        - `ALL PROD AND SANDBOX`
    - Helper:
        - `normalize_platform_selection(selected, platforms_list=None)`  
          expands these special entries into real hostnames and deduplicates them

There are **no** HTTP clients, OAuth, or API calls in this library.

---

## Installing in Google Colab

At the top of your Colab notebook:

```python
# 1. Clone the repo (HTTPS example)
!rm -rf apigw-colab-common
!git clone https://github.com/deniz-yildiz_kyriba/apigw-tools.git apigw-colab-common

# 2. Add it to Python path
import sys
sys.path.append('/content/apigw-colab-common')

# 3. Import the module
import importlib
import apigw_common
importlib.reload(apigw_common)  # optional; handy while iterating
 