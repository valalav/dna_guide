---
description: 
---

## Gemini Added Memories
- Completed Rolling Backtest implementation. Top model is SARIMAX (RMSE 0.3985). BVAR improved to 0.5205 with PyMC/JAX. MS-AR implemented with RMSE 0.5467. XGBoost underperforming at 0.5904. Multi-env orchestration script created: scripts/run_rolling_backtest.py.
- The dashboard runs on port 8501 (Streamlit).
- Parabricks DeepVariant on Tesla V100 with GRCh38.d1.vd1 reference achieved ~5m 47s processing time per sample (targeted calling), significantly faster than CPU (~44m). Next step is fixing Docker file permission issues.
- The BVAR model acts as an 'Oracle' for inflation forecasting in the Opus Forecast project. When its prediction deviates from the ensemble mean by > 0.179, it signals a 1.55x higher risk of forecast error in the *next* month, serving as a volatility early warning system.
- Deflation in Fruit and Vegetable prices (MoM) is a leading indicator (Corr -0.45) of aggregate forecast errors in the subsequent month for the KBR region. This 'Whip Effect' suggests that sharp drops in volatile components precede broader model instability.
