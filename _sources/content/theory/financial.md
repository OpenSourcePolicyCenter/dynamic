
(Chap_FinInt)=

# Financial Intermediary

Domestic household wealth, $W^d_{t}=B_{t}$ and foreign ownership of domestic assets $W^f_{t}$ are invested in a financial intermediary. This intermediary purchases a portfolio of government bonds and private capital in accordance with the domestic and foreign investor demand for these assets and then returns a single portfolio rate of return to all investors.

Foreign demand for government bonds is specified in section {ref}`SecMarkClrMktClr_G` of the {ref}`Chap_MarkClr` chapter:

  ```{math}
  :label: EqMarkClr_zetaD2
    D^{f}_{t+1} = D^{f}_{t} + \zeta_{D}(D_{t+1} - D_{t}) \quad\forall t
  ```

This leaves domestic investors to buy up the residual amount of government debt:

  ```{math}
  :label: EqMarkClr_zetaD2
    D^{d}_{t} = D_{t} - D^{f}_{t} \quad\forall t
  ```

We assume that debt dominates the capital markets, such that domestic investor demand for capital, $K^{d}_{t}$ is given as:

  ```{math}
  :label: eq_domestic_cap_demand
    K^{d}_{t} = B_{t} - D^{d}_{t} \quad\forall t
  ```

Foreign demand for capital is given in {ref}`SecMarkClrMktClr_K`, where $K^{f}_{t}$ is an exogenous fraction of excess capital demand at the world interest rate:

  ```{math}
  :label: eq_foreign_cap_demand
    K^{f}_t = \zeta_{K}ED^{K,r^*}_t \quad\forall t
  ```

The total amount invested in the financial intermediary is thus:

```{math}
W_{t} & = W^d_{t} + W^f_{t} \\
    & = D^d_t + K^d_t  + D^f_t + K^f_t \\
    & = D_t + K_t
```

Interest rates on private capital and government bonds differ.  The return on the portfolio of assets held in the financial intermediary is the weighted average of these two rates of return:

```{math}
:label: eq_portfolio_return
r_{p,t} = \frac{r_{gov,t}D_{t} + r_{t}K_{t}}{D_{t} + K_{t}} \quad\forall t
```
