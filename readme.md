# Random Number Generator
This project contains various generators that can produce numbers from distributions like:
- Natural numbers from 0 to 2147483647 (which is equivalent of 2<sup>31</sup> - 1) marked as "G".
- Uniform on interval from 0 to 1 defined as "J". It is based on results from "G" generator.
- Bernoulli defined as "B". It uses results from "J" generator.
- Binomial defined as "D". It also uses results from "J" generator.
- Poisson marked as "P". Uses generator "J" and "G" to create variable.
- Exponential defined as "W". It uses "J" generator.
- Normal defined as "N". Also uses "J" generator.

 More details about how this generators works and formulas used in exponential and normal distributions are described in ProjectDocumentation.pdf along with Series Test and simple test created by me named MMVK (mean, median, variance, kurtosis) with my thoughts about final results.