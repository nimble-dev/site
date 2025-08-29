library(nimble)
data(faithful)

code <- nimbleCode({
  for(i in 1:n) {
    y[i] ~ dnorm(mu[i], var = s2[i])
    mu[i] <- muTilde[xi[i]]
    s2[i] <- s2Tilde[xi[i]]
  }
  xi[1:n] ~ dCRP(alpha, size = n)
  for(i in 1:n) {
    muTilde[i] ~ dnorm(0, var = s2Tilde[i])
    s2Tilde[i] ~ dinvgamma(2, 1)
  }
  alpha ~ dgamma(1, 1)
})

set.seed(1)
# Model Data
lFaithful <- log(faithful$waiting)
standlFaithful <- (lFaithful - mean(lFaithful)) / sd(lFaithful)
data <- list(y = standlFaithful)
# Model Constants
consts <- list(n = length(standlFaithful))
# Parameter initialization
inits <- list(xi = sample(1:10, size=consts$n, replace=TRUE),
              muTilde = rnorm(consts$n, 0, sd = sqrt(10)),
              s2Tilde = rinvgamma(consts$n, 2, 1),
              alpha = 1)
# Model creation and compilation
rModel <- nimbleModel(code, data = data, inits = inits, constants = consts)
cModel <- compileNimble(rModel)
conf <- configureMCMC(rModel, monitors = c("xi", "muTilde", "s2Tilde", "alpha"))
mcmc <- buildMCMC(conf)
cmcmc <- compileNimble(mcmc, project = rModel)

samples <- runMCMC(cmcmc, niter = 7000, nburnin = 2000, setSeed = TRUE)
outputG <- getSamplesDPmeasure(cmcmc)
