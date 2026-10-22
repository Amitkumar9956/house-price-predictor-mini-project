# Day 1 - Project Setup

## Objective
Learn how to load a dataset using Pandas.

## Topics Covered
- Kaggle Dataset Download
- VS Code Setup
- Pandas Introduction
- Reading CSV File

## Functions Learned

### pd.read_csv()

Purpose:
Read CSV file into a DataFrame.

Syntax

df = pd.read_csv("train.csv")

### df.head()

Shows first five rows.

### df.shape

Returns number of rows and columns.

Example

(1460,81)

### df.columns

Displays all column names.

### df.info()

Displays dataset information.

## What I Learned

- Dataset contains 1460 houses.
- There are 81 columns.
- Target column is SalePrice.

## Errors I Faced

Python could not find main.py because I was in the wrong folder.

Solution:
Changed the terminal directory and ran

python main.py