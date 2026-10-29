# Inverse Function Calculator & Graph Visualizer

A Streamlit web application for calculating inverse expressions, showing a basic
step-by-step solution, plotting the original and inverse expressions, and
performing symbolic composition checks.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Upload `app.py` and `requirements.txt` to a GitHub repository, then deploy the
repository using Streamlit Community Cloud with `app.py` as the main file.

## Input examples

- `2*x + 4`
- `3*x - 5`
- `x**2`
- `sqrt(x)`

Use Python-style notation (`x**2` means x squared).

## Important limitations

This is an educational prototype. Some expressions do not have a global inverse
over their full domain; domain restrictions may be necessary. The input parser
is not intended for arbitrary untrusted input in a production deployment.
