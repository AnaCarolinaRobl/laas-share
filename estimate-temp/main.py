import pandas as pd
import statsmodels.api as sm

#create DataFrame
df = pd.DataFrame({'hours': [1, 1, 2, 2, 2, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 8],
                   'score': [48, 78, 72, 70, 66, 92, 93, 75, 75, 80, 95, 97,
                             90, 96, 99, 99]})

#view first five rows of DataFrame
print(df.head())


#define predictor and response variables
y = df['score']
X = df['hours']

#add constant to predictor variables
X = sm.add_constant(X)

#fit linear regression model
fit = sm.OLS(y, X).fit()

#view model summary
print(fit.summary())

#define weights to use
wt = 1 / sm.OLS('fit.resid.abs() ~ fit.fittedvalues', data=df).fit().fittedvalues**2

#fit weighted least squares regression model
fit_wls = sm.WLS(y, X, weights=wt).fit()

#view summary of weighted least squares regression model
print(fit_wls.summary())