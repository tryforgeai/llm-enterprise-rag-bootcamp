# PRML Chapter 2: Probability Distributions

Source: `course/week_03/data/PRML.pdf`
Book pages: 67-136
Extracted PDF pages: 86-155

> Text extracted mechanically from the local PDF for Week 04 abstractive summarization, chunking, QA-pair, and retrieval experiments.


## PDF Page 86

2
Probability
Distributions
In Chapter 1, we emphasized the central role played by probability theory in the
solution of pattern recognition problems. We turn now to an exploration of some
particular examples of probability distributions and their properties. As well as be-
ing of great interest in their own right, these distributions can form building blocks
for more complex models and will be used extensively throughout the book. The
distributions introduced in this chapter will also serve another important purpose,
namely to provide us with the opportunity to discuss some key statistical concepts,
such as Bayesian inference, in the context of simple models before we encounter
them in more complex situations in later chapters.
One role for the distributions discussed in this chapter is to model the prob-
ability distribution p(x) of a random variable x, given a ﬁnite set x
1,..., xN of
observations. This problem is known as density estimation . For the purposes of
this chapter, we shall assume that the data points are independent and identically
distributed. It should be emphasized that the problem of density estimation is fun-
67


## PDF Page 87

68 2. PROBABILITY DISTRIBUTIONS
damentally ill-posed, because there are inﬁnitely many probability distributions that
could have given rise to the observed ﬁnite data set. Indeed, any distribution p(x)
that is nonzero at each of the data points x1,..., xN is a potential candidate. The
issue of choosing an appropriate distribution relates to the problem of model selec-
tion that has already been encountered in the context of polynomial curve ﬁtting in
Chapter 1 and that is a central issue in pattern recognition.
We begin by considering the binomial and multinomial distributions for discrete
random variables and the Gaussian distribution for continuous random variables.
These are speciﬁc examples of parametric distributions, so-called because they are
governed by a small number of adaptive parameters, such as the mean and variance in
the case of a Gaussian for example. To apply such models to the problem of density
estimation, we need a procedure for determining suitable values for the parameters,
given an observed data set. In a frequentist treatment, we choose speciﬁc values
for the parameters by optimizing some criterion, such as the likelihood function. By
contrast, in a Bayesian treatment we introduce prior distributions over the parameters
and then use Bayes’ theorem to compute the corresponding posterior distribution
given the observed data.
We shall see that an important role is played by conjugate priors, that lead to
posterior distributions having the same functional form as the prior, and that there-
fore lead to a greatly simpliﬁed Bayesian analysis. For example, the conjugate prior
for the parameters of the multinomial distribution is called the Dirichlet distribution,
while the conjugate prior for the mean of a Gaussian is another Gaussian. All of these
distributions are examples of the exponential family of distributions, which possess
a number of important properties, and which will be discussed in some detail.
One limitation of the parametric approach is that it assumes a speciﬁc functional
form for the distribution, which may turn out to be inappropriate for a particular
application. An alternative approach is given by nonparametric density estimation
methods in which the form of the distribution typically depends on the size of the data
set. Such models still contain parameters, but these control the model complexity
rather than the form of the distribution. We end this chapter by considering three
nonparametric methods based respectively on histograms, nearest-neighbours, and
kernels.
2.1. Binary Variables
We begin by considering a single binary random variable x ∈{ 0, 1}. For example,
x might describe the outcome of ﬂipping a coin, with x =1 representing ‘heads’,
and x =0 representing ‘tails’. We can imagine that this is a damaged coin so that
the probability of landing heads is not necessarily the same as that of landing tails.
The probability of x =1 will be denoted by the parameter µ so that
p(x =1 |µ)=µ (2.1)


## PDF Page 88

2.1. Binary Variables 69
where 0 ⩽ µ ⩽ 1, from which it follows that p(x =0 |µ)=1 − µ. The probability
distribution over x can therefore be written in the form
Bern(x|µ)= µx(1 − µ)1−x (2.2)
which is known as the Bernoulli distribution. It is easily veriﬁed that this distributionExercise 2.1
is normalized and that it has mean and variance given by
E[x]= µ (2.3)
var[x]= µ(1 − µ). (2.4)
Now suppose we have a data set D = {x1,...,x N } of observed values of x.
We can construct the likelihood function, which is a function of µ, on the assumption
that the observations are drawn independently from p(x|µ), so that
p(D|µ)=
N∏
n=1
p(xn|µ)=
N∏
n=1
µxn (1 − µ)1−xn . (2.5)
In a frequentist setting, we can estimate a value for µ by maximizing the likelihood
function, or equivalently by maximizing the logarithm of the likelihood. In the case
of the Bernoulli distribution, the log likelihood function is given by
lnp(D|µ)=
N∑
n=1
ln p(xn|µ)=
N∑
n=1
{xn ln µ +( 1 − xn)l n ( 1− µ)} . (2.6)
At this point, it is worth noting that the log likelihood function depends on the N
observations xn only through their sum ∑
n xn. This sum provides an example of a
sufﬁcient statistic for the data under this distribution, and we shall study the impor-
tant role of sufﬁcient statistics in some detail. If we set the derivative of lnp(D|µ)Section 2.4
with respect to µ equal to zero, we obtain the maximum likelihood estimator
µML = 1
N
N∑
n=1
xn (2.7)
Jacob Bernoulli
1654–1705
Jacob Bernoulli, also known as
Jacques or James Bernoulli, was a
Swiss mathematician and was the
ﬁrst of many in the Bernoulli family
to pursue a career in science and
mathematics. Although compelled
to study philosophy and theology against his will by
his parents, he travelled extensively after graduating
in order to meet with many of the leading scientists of
his time, including Boyle and Hooke in England. When
he returned to Switzerland, he taught mechanics and
became Professor of Mathematics at Basel in 1687.
Unfortunately, rivalry between Jacob and his younger
brother Johann turned an initially productive collabora-
tion into a bitter and public dispute. Jacob’s most sig-
niﬁcant contributions to mathematics appeared in
The
Art of Conjecture published in 1713, eight years after
his death, which deals with topics in probability the-
ory including what has become known as the Bernoulli
distribution.


## PDF Page 89

70 2. PROBABILITY DISTRIBUTIONS
Figure 2.1 Histogram plot of the binomial dis-
tribution (2.9) as a function of m for
N =1 0 and µ =0 .25.
m
0 1 2 3 4 5 6 7 8 9 10
0
0.1
0.2
0.3
which is also known as the sample mean. If we denote the number of observations
of x =1 (heads) within this data set by m, then we can write (2.7) in the form
µML = m
N (2.8)
so that the probability of landing heads is given, in this maximum likelihood frame-
work, by the fraction of observations of heads in the data set.
Now suppose we ﬂip a coin, say, 3 times and happen to observe 3 heads. Then
N = m =3 and µML =1 . In this case, the maximum likelihood result would
predict that all future observations should give heads. Common sense tells us that
this is unreasonable, and in fact this is an extreme example of the over-ﬁtting associ-
ated with maximum likelihood. We shall see shortly how to arrive at more sensible
conclusions through the introduction of a prior distribution over µ.
We can also work out the distribution of the number m of observations of x =1 ,
given that the data set has size N . This is called the binomial distribution, and
from (2.5) we see that it is proportional to µ
m(1 − µ)N −m. In order to obtain the
normalization coefﬁcient we note that out of N coin ﬂips, we have to add up all
of the possible ways of obtaining m heads, so that the binomial distribution can be
written
Bin(m|N,µ )=
(N
m
)
µm(1 − µ)N −m (2.9)
where (N
m
)
≡ N!
(N − m)!m! (2.10)
is the number of ways of choosing m objects out of a total of N identical objects.Exercise 2.3
Figure 2.1 shows a plot of the binomial distribution for N =1 0 and µ =0 .25.
The mean and variance of the binomial distribution can be found by using the
result of Exercise 1.10, which shows that for independent events the mean of the
sum is the sum of the means, and the variance of the sum is the sum of the variances.
Because m = x1 + ... + xN , and for each observation the mean and variance are


## PDF Page 90

2.1. Binary Variables 71
given by (2.3) and (2.4), respectively, we have
E[m] ≡
N∑
m=0
mBin(m|N,µ )=Nµ (2.11)
var[m] ≡
N∑
m=0
(m − E[m])2 Bin(m|N,µ )=Nµ (1 − µ). (2.12)
These results can also be proved directly using calculus.Exercise 2.4
2.1.1 The beta distribution
We have seen in (2.8) that the maximum likelihood setting for the parameter µ
in the Bernoulli distribution, and hence in the binomial distribution, is given by the
fraction of the observations in the data set having x =1 . As we have already noted,
this can give severely over-ﬁtted results for small data sets. In order to develop a
Bayesian treatment for this problem, we need to introduce a prior distribution p(µ)
over the parameter µ. Here we consider a form of prior distribution that has a simple
interpretation as well as some useful analytical properties. To motivate this prior,
we note that the likelihood function takes the form of the product of factors of the
form µ
x(1 − µ)1−x. If we choose a prior to be proportional to powers of µ and
(1 − µ), then the posterior distribution, which is proportional to the product of the
prior and the likelihood function, will have the same functional form as the prior.
This property is called conjugacy and we will see several examples of it later in this
chapter. We therefore choose a prior, called the beta distribution, given by
Beta(µ|a, b)= Γ(a + b)
Γ(a)Γ(b)µa−1(1 − µ)b−1 (2.13)
where Γ(x) is the gamma function deﬁned by (1.141), and the coefﬁcient in (2.13)
ensures that the beta distribution is normalized, so thatExercise 2.5
∫ 1
0
Beta(µ|a, b)d µ =1 . (2.14)
The mean and variance of the beta distribution are given byExercise 2.6
E[µ]= a
a + b (2.15)
var[µ]= ab
(a + b)2(a + b +1 ). (2.16)
The parameters a and b are often called hyperparameters because they control the
distribution of the parameter µ. Figure 2.2 shows plots of the beta distribution for
various values of the hyperparameters.
The posterior distribution of µ is now obtained by multiplying the beta prior
(2.13) by the binomial likelihood function (2.9) and normalizing. Keeping only the
factors that depend on µ, we see that this posterior distribution has the form
p(µ|m, l, a, b) ∝ µ
m+a−1(1 − µ)l+b−1 (2.17)


## PDF Page 91

72 2. PROBABILITY DISTRIBUTIONS
µ
a =0 .1
b =0 .1
0 0.5 1
0
1
2
3
µ
a =1
b =1
0 0.5 1
0
1
2
3
µ
a =2
b =3
0 0.5 1
0
1
2
3
µ
a =8
b =4
0 0.5 1
0
1
2
3
Figure 2.2 Plots of the beta distribution Beta(µ|a, b) given by (2.13) as a function of µ for various values of the
hyperparameters a and b.
where l = N − m, and therefore corresponds to the number of ‘tails’ in the coin
example. We see that (2.17) has the same functional dependence on µ as the prior
distribution, reﬂecting the conjugacy properties of the prior with respect to the like-
lihood function. Indeed, it is simply another beta distribution, and its normalization
coefﬁcient can therefore be obtained by comparison with (2.13) to give
p(µ|m, l, a, b)= Γ(m + a + l + b)
Γ(m + a)Γ(l + b)µm+a−1(1 − µ)l+b−1. (2.18)
We see that the effect of observing a data set of m observations of x =1 and
l observations of x =0 has been to increase the value of a by m, and the value of
b by l, in going from the prior distribution to the posterior distribution. This allows
us to provide a simple interpretation of the hyperparameters a and b in the prior as
an effective number of observations of x =1 and x =0 , respectively. Note that
a and b need not be integers. Furthermore, the posterior distribution can act as the
prior if we subsequently observe additional data. To see this, we can imagine taking
observations one at a time and after each observation updating the current posterior


## PDF Page 92

2.1. Binary Variables 73
µ
prior
0 0.5 1
0
1
2
µ
likelihood function
0 0.5 1
0
1
2
µ
posterior
0 0.5 1
0
1
2
Figure 2.3 Illustration of one step of sequential Bayesian inference. The prior is given by a beta distribution
with parameters a =2 , b =2 , and the likelihood function, given by (2.9) with N = m =1 , corresponds to a
single observation of x =1 , so that the posterior is given by a beta distribution with parameters a =3 , b =2 .
distribution by multiplying by the likelihood function for the new observation and
then normalizing to obtain the new, revised posterior distribution. At each stage, the
posterior is a beta distribution with some total number of (prior and actual) observed
values for x =1 and x =0 given by the parameters a and b. Incorporation of an
additional observation of x =1 simply corresponds to incrementing the value of a
by 1, whereas for an observation of x =0 we increment b by 1. Figure 2.3 illustrates
one step in this process.
We see that this sequential approach to learning arises naturally when we adopt
a Bayesian viewpoint. It is independent of the choice of prior and of the likelihood
function and depends only on the assumption of i.i.d. data. Sequential methods make
use of observations one at a time, or in small batches, and then discard them before
the next observations are used. They can be used, for example, in real-time learning
scenarios where a steady stream of data is arriving, and predictions must be made
before all of the data is seen. Because they do not require the whole data set to be
stored or loaded into memory, sequential methods are also useful for large data sets.
Maximum likelihood methods can also be cast into a sequential framework.Section 2.3.5
If our goal is to predict, as best we can, the outcome of the next trial, then we
must evaluate the predictive distribution of x, given the observed data set D. From
the sum and product rules of probability, this takes the form
p(x =1 |D)=
∫ 1
0
p(x =1 |µ)p(µ|D)d µ =
∫ 1
0
µp(µ|D)d µ = E[µ|D]. (2.19)
Using the result (2.18) for the posterior distribution p(µ|D), together with the result
(2.15) for the mean of the beta distribution, we obtain
p(x =1 |D)= m + a
m + a + l + b (2.20)
which has a simple interpretation as the total fraction of observations (both real ob-
servations and ﬁctitious prior observations) that correspond to x =1 . Note that in
the limit of an inﬁnitely large data set m, l →∞ the result (2.20) reduces to the
maximum likelihood result (2.8). As we shall see, it is a very general property that
the Bayesian and maximum likelihood results will agree in the limit of an inﬁnitely


## PDF Page 93

74 2. PROBABILITY DISTRIBUTIONS
large data set. For a ﬁnite data set, the posterior mean for µ always lies between the
prior mean and the maximum likelihood estimate for µ corresponding to the relative
frequencies of events given by (2.7).Exercise 2.7
From Figure 2.2, we see that as the number of observations increases, so the
posterior distribution becomes more sharply peaked. This can also be seen from
the result (2.16) for the variance of the beta distribution, in which we see that the
variance goes to zero for a →∞ or b →∞ . In fact, we might wonder whether it is
a general property of Bayesian learning that, as we observe more and more data, the
uncertainty represented by the posterior distribution will steadily decrease.
To address this, we can take a frequentist view of Bayesian learning and show
that, on average, such a property does indeed hold. Consider a general Bayesian
inference problem for a parameter θ for which we have observed a data set D, de-
scribed by the joint distribution p(θ, D). The following resultExercise 2.8
Eθ[θ]= ED [Eθ[θ|D]] (2.21)
where
Eθ[θ] ≡
∫
p(θ)θdθ (2.22)
ED[Eθ[θ|D]] ≡
∫ { ∫
θp(θ|D)d θ
}
p(D)d D (2.23)
says that the posterior mean of θ, averaged over the distribution generating the data,
is equal to the prior mean of θ. Similarly, we can show that
varθ[θ]=E D [varθ[θ|D]] + varD [Eθ[θ|D]]. (2.24)
The term on the left-hand side of (2.24) is the prior variance of θ. On the right-
hand side, the ﬁrst term is the average posterior variance of θ, and the second term
measures the variance in the posterior mean of θ. Because this variance is a positive
quantity, this result shows that, on average, the posterior variance of θ is smaller than
the prior variance. The reduction in variance is greater if the variance in the posterior
mean is greater. Note, however, that this result only holds on average, and that for a
particular observed data set it is possible for the posterior variance to be larger than
the prior variance.
2.2. Multinomial Variables
Binary variables can be used to describe quantities that can take one of two possible
values. Often, however, we encounter discrete variables that can take on one of K
possible mutually exclusive states. Although there are various alternative ways to
express such variables, we shall see shortly that a particularly convenient represen-
tation is the 1-of-K scheme in which the variable is represented by a K-dimensional
vector x in which one of the elements x
k equals 1, and all remaining elements equal


## PDF Page 94

2.2. Multinomial Variables 75
0. So, for instance if we have a variable that can take K =6 states and a particular
observation of the variable happens to correspond to the state where x3 =1 , then x
will be represented by
x =( 0, 0, 1, 0, 0, 0)T. (2.25)
Note that such vectors satisfy ∑K
k=1 xk =1 . If we denote the probability of xk =1
by the parameter µk, then the distribution of x is given
p(x|µ)=
K∏
k=1
µxk
k (2.26)
where µ =( µ1,...,µ K)T, and the parameters µk are constrained to satisfy µk ⩾ 0
and ∑
k µk =1 , because they represent probabilities. The distribution (2.26) can be
regarded as a generalization of the Bernoulli distribution to more than two outcomes.
It is easily seen that the distribution is normalized
∑
x
p(x|µ)=
K∑
k=1
µk =1 (2.27)
and that
E[x|µ]=
∑
x
p(x|µ)x =( µ1,...,µ M )T = µ. (2.28)
Now consider a data set D of N independent observations x1,..., xN . The
corresponding likelihood function takes the form
p(D|µ)=
N∏
n=1
K∏
k=1
µxnk
k =
K∏
k=1
µ(
P
n xnk)
k =
K∏
k=1
µmk
k . (2.29)
We see that the likelihood function depends on the N data points only through the
K quantities
mk =
∑
n
xnk (2.30)
which represent the number of observations of xk =1 . These are called the sufﬁcient
statistics for this distribution.Section 2.4
In order to ﬁnd the maximum likelihood solution for µ, we need to maximize
lnp(D|µ) with respect to µk taking account of the constraint that the µk must sum
to one. This can be achieved using a Lagrange multiplier λ and maximizingAppendix E
K∑
k=1
mk lnµk + λ
( K∑
k=1
µk − 1
)
. (2.31)
Setting the derivative of (2.31) with respect to µk to zero, we obtain
µk = −mk/λ. (2.32)


## PDF Page 95

76 2. PROBABILITY DISTRIBUTIONS
We can solve for the Lagrange multiplier λ by substituting (2.32) into the constraint∑
k µk =1 to give λ = −N . Thus we obtain the maximum likelihood solution in
the form
µML
k = mk
N (2.33)
which is the fraction of the N observations for which xk =1 .
We can consider the joint distribution of the quantitiesm1,...,m K , conditioned
on the parameters µ and on the total number N of observations. From (2.29) this
takes the form
Mult(m1,m2,...,m K |µ,N )=
( N
m1m2 ...m K
) K∏
k=1
µmk
k (2.34)
which is known as the multinomial distribution. The normalization coefﬁcient is the
number of ways of partitioning N objects into K groups of size m1,...,m K and is
given by ( N
m1m2 ...m K
)
= N!
m1!m2! ...m K!. (2.35)
Note that the variables mk are subject to the constraint
K∑
k=1
mk = N. (2.36)
2.2.1 The Dirichlet distribution
We now introduce a family of prior distributions for the parameters {µk} of
the multinomial distribution (2.34). By inspection of the form of the multinomial
distribution, we see that the conjugate prior is given by
p(µ|α) ∝
K∏
k=1
µαk −1
k (2.37)
where 0 ⩽ µk ⩽ 1 and ∑
k µk =1 . Here α1,...,α K are the parameters of the
distribution, and α denotes (α1,...,α K)T. Note that, because of the summation
constraint, the distribution over the space of the {µk} is conﬁned to a simplex of
dimensionality K − 1, as illustrated for K =3 in Figure 2.4.
The normalized form for this distribution is byExercise 2.9
Dir(µ|α)= Γ(α0)
Γ(α1) ··· Γ(αK)
K∏
k=1
µαk −1
k (2.38)
which is called the Dirichlet distribution. Here Γ(x) is the gamma function deﬁned
by (1.141) while
α0 =
K∑
k=1
αk. (2.39)


## PDF Page 96

2.2. Multinomial Variables 77
Figure 2.4 The Dirichlet distribution over three variables µ1,µ 2,µ 3
is conﬁned to a simplex (a bounded linear manifold) of
the form shown, as a consequence of the constraints
0 ⩽ µk ⩽ 1 and P
k µk =1 .
µ1
µ2
µ3
Plots of the Dirichlet distribution over the simplex, for various settings of the param-
eters αk, are shown in Figure 2.5.
Multiplying the prior (2.38) by the likelihood function (2.34), we obtain the
posterior distribution for the parameters {µk} in the form
p(µ|D, α) ∝ p(D|µ)p(µ|α) ∝
K∏
k=1
µαk+mk −1
k . (2.40)
We see that the posterior distribution again takes the form of a Dirichlet distribution,
conﬁrming that the Dirichlet is indeed a conjugate prior for the multinomial. This
allows us to determine the normalization coefﬁcient by comparison with (2.38) so
that
p(µ|D, α)=D i r ( µ|α + m)
= Γ(α
0 + N)
Γ(α1 + m1) ··· Γ(αK + mK)
K∏
k=1
µαk+mk −1
k (2.41)
where we have denoted m =( m1,...,m K)T. As for the case of the binomial
distribution with its beta prior, we can interpret the parameters αk of the Dirichlet
prior as an effective number of observations of xk =1 .
Note that two-state quantities can either be represented as binary variables and
Lejeune Dirichlet
1805–1859
Johann Peter Gustav Lejeune
Dirichlet was a modest and re-
served mathematician who made
contributions in number theory, me-
chanics, and astronomy, and who
gave the ﬁrst rigorous analysis of
Fourier series. His family originated from Richelet
in Belgium, and the name Lejeune Dirichlet comes
from ‘le jeune de Richelet’ (the young person from
Richelet). Dirichlet’s ﬁrst paper, which was published
in 1825, brought him instant fame. It concerned Fer-
mat’s last theorem, which claims that there are no
positive integer solutions to x
n + yn = zn for n>2.
Dirichlet gave a partial proof for the casen =5 , which
was sent to Legendre for review and who in turn com-
pleted the proof. Later, Dirichlet gave a complete proof
for n =1 4, although a full proof of Fermat’s last theo-
rem for arbitrary n had to wait until the work of Andrew
Wiles in the closing years of the 20
th century.


## PDF Page 97

78 2. PROBABILITY DISTRIBUTIONS
Figure 2.5 Plots of the Dirichlet distribution over three vari ables, where the two horizontal axes are coordinates
in the plane of the simplex and the vertical axis corresponds to the value of the density . Here {αk } =0 .1 on the
left plot, {αk } =1 in the centre plot, and {αk } =1 0 in the right plot.
modelled using the binomial distribution (2.9) or as 1-of-2 variables and modelled
using the multinomial distribution (2.34) with K =2 .
2.3.
 The Gaussian Distribution
The Gaussian, also known as the normal distribution, is a widely used model for the
distribution of continuous variables. In the case of a single variable x, the Gaussian
distribution can be written in the form
N(x|µ, σ
2)= 1
(2πσ2)1/2 exp
{
− 1
2σ2 (x − µ)2
}
(2.42)
where µ is the mean and σ2 is the variance. For a D-dimensional vector x,t h e
multivariate Gaussian distribution takes the form
N(x|µ,Σ)= 1
(2π)D/2
1
|Σ|1/2 exp
{
− 1
2(x − µ)TΣ−1(x − µ)
}
(2.43)
where µ is a D-dimensional mean vector, Σ is a D × D covariance matrix, and |Σ|
denotes the determinant of Σ.
The Gaussian distribution arises in many different contexts and can be motivated
from a variety of different perspectives. For example, we have already seen that forSection 1.6
a single real variable, the distribution that maximizes the entropy is the Gaussian.
This property applies also to the multivariate Gaussian.Exercise 2.14
Another situation in which the Gaussian distribution arises is when we consider
the sum of multiple random variables. The central limit theorem (due to Laplace)
tells us that, subject to certain mild conditions, the sum of a set of random variables,
which is of course itself a random variable, has a distribution that becomes increas-
ingly Gaussian as the number of terms in the sum increases (Walker, 1969). We can


## PDF Page 98

2.3. The Gaussian Distribution 79
N =1
0 0.5 1
0
1
2
3 N =2
0 0.5 1
0
1
2
3 N =1 0
0 0.5 1
0
1
2
3
Figure 2.6 Histogram plots of the mean of N uniformly distributed numbers for various values of N.W e
observe that as N increases, the distribution tends towards a Gaussian.
illustrate this by considering N variables x1,...,x N each of which has a uniform
distribution over the interval [0, 1] and then considering the distribution of the mean
(x1 + ··· + xN )/N. For large N, this distribution tends to a Gaussian, as illustrated
in Figure 2.6. In practice, the convergence to a Gaussian as N increases can be
very rapid. One consequence of this result is that the binomial distribution (2.9),
which is a distribution over m deﬁned by the sum of N observations of the random
binary variable x, will tend to a Gaussian as N →∞ (see Figure 2.1 for the case of
N =1 0).
The Gaussian distribution has many important analytical properties, and we shall
consider several of these in detail. As a result, this section will be rather more tech-
nically involved than some of the earlier sections, and will require familiarity with
various matrix identities. However, we strongly encourage the reader to become pro-Appendix C
ﬁcient in manipulating Gaussian distributions using the techniques presented here as
this will prove invaluable in understanding the more complex models presented in
later chapters.
We begin by considering the geometrical form of the Gaussian distribution. The
Carl Friedrich Gauss
1777–1855
It is said that when Gauss went
to elementary school at age 7, his
teacher B ¨uttner, trying to keep the
class occupied, asked the pupils to
sum the integers from 1 to 100. To
the teacher’s amazement, Gauss
arrived at the answer in a matter of moments by noting
that the sum can be represented as 50 pairs (1 + 100,
2+99, etc.) each of which added to 101, giving the an-
swer 5,050. It is now believed that the problem which
was actually set was of the same form but somewhat
harder in that the sequence had a larger starting value
and a larger increment. Gauss was a German math-
ematician and scientist with a reputation for being a
hard-working perfectionist. One of his many contribu-
tions was to show that least squares can be derived
under the assumption of normally distributed errors.
He also created an early formulation of non-Euclidean
geometry (a self-consistent geometrical theory that vi-
olates the axioms of Euclid) but was reluctant to dis-
cuss it openly for fear that his reputation might suffer
if it were seen that he believed in such a geometry.
At one point, Gauss was asked to conduct a geodetic
survey of the state of Hanover, which led to his for-
mulation of the normal distribution, now also known
as the Gaussian. After his death, a study of his di-
aries revealed that he had discovered several impor-
tant mathematical results years or even decades be-
fore they were published by others.


## PDF Page 99

80 2. PROBABILITY DISTRIBUTIONS
functional dependence of the Gaussian on x is through the quadratic form
∆2 =( x − µ)TΣ−1(x − µ) (2.44)
which appears in the exponent. The quantity ∆ is called the Mahalanobis distance
from µ to x and reduces to the Euclidean distance whenΣ is the identity matrix. The
Gaussian distribution will be constant on surfaces inx-space for which this quadratic
form is constant.
First of all, we note that the matrix Σ can be taken to be symmetric, without
loss of generality, because any antisymmetric component would disappear from the
exponent. Now consider the eigenvector equation for the covariance matrixExercise 2.17
Σui = λiui (2.45)
where i =1 ,...,D . Because Σ is a real, symmetric matrix its eigenvalues will be
real, and its eigenvectors can be chosen to form an orthonormal set, so thatExercise 2.18
uT
i uj = Iij (2.46)
where Iij is the i, j element of the identity matrix and satisﬁes
Iij =
{
1, if i = j
0, otherwise. (2.47)
The covariance matrix Σ can be expressed as an expansion in terms of its eigenvec-
tors in the formExercise 2.19
Σ =
D∑
i=1
λiuiuT
i (2.48)
and similarly the inverse covariance matrixΣ−1 can be expressed as
Σ−1 =
D∑
i=1
1
λi
uiuT
i . (2.49)
Substituting (2.49) into (2.44), the quadratic form becomes
∆2 =
D∑
i=1
y2
i
λi
(2.50)
where we have deﬁned
yi = uT
i (x − µ). (2.51)
We can interpret{yi} as a new coordinate system deﬁned by the orthonormal vectors
ui that are shifted and rotated with respect to the original xi coordinates. Forming
the vector y =( y1,...,y D)T,w eh a v e
y = U(x − µ) (2.52)


## PDF Page 100

2.3. The Gaussian Distribution 81
Figure 2.7 The red curve shows the ellip-
tical surface of constant proba-
bility density for a Gaussian in
a two-dimensional space x =
(x1,x 2) on which the density
is exp(−1/2) of its value at
x = µ. The major axes of
the ellipse are deﬁned by the
eigenvectors u
i of the covari-
ance matrix, with correspond-
ing eigenvalues λ
i.
x1
x2
λ1/2
1
λ1/2
2
y1
y2
u1
u2
µ
where U is a matrix whose rows are given by uT
i . From (2.46) it follows that U is
an orthogonal matrix, i.e., it satisﬁes UUT = I, and hence also UTU = I, where IAppendix C
is the identity matrix.
The quadratic form, and hence the Gaussian density, will be constant on surfaces
for which (2.51) is constant. If all of the eigenvalues λi are positive, then these
surfaces represent ellipsoids, with their centres atµ and their axes oriented alongui,
and with scaling factors in the directions of the axes given by λ1/2
i , as illustrated in
Figure 2.7.
For the Gaussian distribution to be well deﬁned, it is necessary for all of the
eigenvalues λi of the covariance matrix to be strictly positive, otherwise the dis-
tribution cannot be properly normalized. A matrix whose eigenvalues are strictly
positive is said to be positive deﬁnite . In Chapter 12, we will encounter Gaussian
distributions for which one or more of the eigenvalues are zero, in which case the
distribution is singular and is conﬁned to a subspace of lower dimensionality. If all
of the eigenvalues are nonnegative, then the covariance matrix is said to be positive
semideﬁnite.
Now consider the form of the Gaussian distribution in the new coordinate system
deﬁned by the yi. In going from thex to they coordinate system, we have a Jacobian
matrix J with elements given by
Jij = ∂xi
∂yj
= Uji (2.53)
where Uji are the elements of the matrix UT. Using the orthonormality property of
the matrix U, we see that the square of the determinant of the Jacobian matrix is
|J|2 =
⏐⏐UT⏐
⏐
2
=
⏐
⏐
UT⏐
⏐
|U| =
⏐
⏐
UTU
⏐
⏐
= |I| =1 (2.54)
and hence |J| =1 . Also, the determinant |Σ| of the covariance matrix can be written


## PDF Page 101

82 2. PROBABILITY DISTRIBUTIONS
as the product of its eigenvalues, and hence
|Σ|1/2 =
D∏
j=1
λ1/2
j . (2.55)
Thus in the yj coordinate system, the Gaussian distribution takes the form
p(y)=p(x)|J| =
D∏
j=1
1
(2πλj)1/2 exp
{
− y2
j
2λj
}
(2.56)
which is the product of D independent univariate Gaussian distributions. The eigen-
vectors therefore deﬁne a new set of shifted and rotated coordinates with respect
to which the joint probability distribution factorizes into a product of independent
distributions. The integral of the distribution in the y coordinate system is then
∫
p(y)dy =
D∏
j=1
∫ ∞
−∞
1
(2πλj)1/2 exp
{
− y2
j
2λj
}
dyj =1 (2.57)
where we have used the result (1.48) for the normalization of the univariate Gaussian.
This conﬁrms that the multivariate Gaussian (2.43) is indeed normalized.
We now look at the moments of the Gaussian distribution and thereby provide an
interpretation of the parameters µ and Σ. The expectation of x under the Gaussian
distribution is given by
E[x]= 1
(2π)D/2
1
|Σ|1/2
∫
exp
{
− 1
2(x − µ)TΣ−1(x − µ)
}
xdx
= 1
(2π)D/2
1
|Σ|1/2
∫
exp
{
− 1
2zTΣ−1z
}
(z + µ)dz (2.58)
where we have changed variables using z = x − µ. We now note that the exponent
is an even function of the components of z and, because the integrals over these are
taken over the range (−∞ , ∞), the term in z in the factor (z + µ) will vanish by
symmetry. Thus
E[x]= µ (2.59)
and so we refer to µ as the mean of the Gaussian distribution.
We now consider second order moments of the Gaussian. In the univariate case,
we considered the second order moment given by E[x2]. For the multivariate Gaus-
sian, there are D2 second order moments given by E[xixj], which we can group
together to form the matrix E[xxT]. This matrix can be written as
E[xxT]= 1
(2π)D/2
1
|Σ|1/2
∫
exp
{
− 1
2(x − µ)TΣ−1(x − µ)
}
xxT dx
= 1
(2π)D/2
1
|Σ|1/2
∫
exp
{
− 1
2zTΣ−1z
}
(z + µ)(z + µ)T dz


## PDF Page 102

2.3. The Gaussian Distribution 83
where again we have changed variables using z = x − µ. Note that the cross-terms
involving µzT and µTz will again vanish by symmetry. The term µµT is constant
and can be taken outside the integral, which itself is unity because the Gaussian
distribution is normalized. Consider the term involving zzT. Again, we can make
use of the eigenvector expansion of the covariance matrix given by (2.45), together
with the completeness of the set of eigenvectors, to write
z =
D∑
j=1
yjuj (2.60)
where yj = uT
j z, which gives
1
(2π)D/2
1
|Σ|1/2
∫
exp
{
− 1
2zTΣ−1z
}
zzT dz
= 1
(2π)D/2
1
|Σ|1/2
D∑
i=1
D∑
j=1
uiuT
j
∫
exp
{
−
D∑
k=1
y2
k
2λk
}
yiyj dy
=
D∑
i=1
uiuT
i λi = Σ (2.61)
where we have made use of the eigenvector equation (2.45), together with the fact
that the integral on the right-hand side of the middle line vanishes by symmetry
unless i = j, and in the ﬁnal line we have made use of the results (1.50) and (2.55),
together with (2.48). Thus we have
E[xx
T]=µµ T + Σ. (2.62)
For single random variables, we subtracted the mean before taking second mo-
ments in order to deﬁne a variance. Similarly, in the multivariate case it is again
convenient to subtract off the mean, giving rise to thecovariance of a random vector
x deﬁned by
cov[x]= E
[
(x − E[x])(x − E[x])T]
. (2.63)
For the speciﬁc case of a Gaussian distribution, we can make use of E[x]= µ,
together with the result (2.62), to give
cov[x]= Σ. (2.64)
Because the parameter matrix Σ governs the covariance of x under the Gaussian
distribution, it is called the covariance matrix.
Although the Gaussian distribution (2.43) is widely used as a density model, it
suffers from some signiﬁcant limitations. Consider the number of free parameters in
the distribution. A general symmetric covariance matrix Σ will have D(D +1 )/2
independent parameters, and there are another D independent parameters in µ,g i v -Exercise 2.21
ing D(D +3 )/2 parameters in total. For large D, the total number of parameters


## PDF Page 103

84 2. PROBABILITY DISTRIBUTIONS
Figure 2.8 Contours of constant
probability density for a Gaussian
distribution in two dimensions in
which the covariance matrix is (a) of
general form, (b) diagonal, in which
the elliptical contours are aligned
with the coordinate axes, and (c)
proportional to the identity matrix, in
which the contours are concentric
circles.
x1
x2
(a)
x1
x2
(b)
x1
x2
(c)
therefore grows quadratically with D, and the computational task of manipulating
and inverting large matrices can become prohibitive. One way to address this prob-
lem is to use restricted forms of the covariance matrix. If we consider covariance
matrices that are diagonal, so that Σ = diag(σ
2
i ), we then have a total of 2D inde-
pendent parameters in the density model. The corresponding contours of constant
density are given by axis-aligned ellipsoids. We could further restrict the covariance
matrix to be proportional to the identity matrix, Σ = σ
2I, known as an isotropic co-
variance, giving D +1 independent parameters in the model and spherical surfaces
of constant density. The three possibilities of general, diagonal, and isotropic covari-
ance matrices are illustrated in Figure 2.8. Unfortunately, whereas such approaches
limit the number of degrees of freedom in the distribution and make inversion of the
covariance matrix a much faster operation, they also greatly restrict the form of the
probability density and limit its ability to capture interesting correlations in the data.
A further limitation of the Gaussian distribution is that it is intrinsically uni-
modal (i.e., has a single maximum) and so is unable to provide a good approximation
to multimodal distributions. Thus the Gaussian distribution can be both too ﬂexible,
in the sense of having too many parameters, while also being too limited in the range
of distributions that it can adequately represent. We will see later that the introduc-
tion of latent variables, also called hidden variables or unobserved variables, allows
both of these problems to be addressed. In particular, a rich family of multimodal
distributions is obtained by introducing discrete latent variables leading to mixtures
of Gaussians, as discussed in Section 2.3.9. Similarly, the introduction of continuous
latent variables, as described in Chapter 12, leads to models in which the number of
free parameters can be controlled independently of the dimensionality D of the data
space while still allowing the model to capture the dominant correlations in the data
set. Indeed, these two approaches can be combined and further extended to derive
a very rich set of hierarchical models that can be adapted to a broad range of prac-
tical applications. For instance, the Gaussian version of the Markov random ﬁeld ,Section 8.3
which is widely used as a probabilistic model of images, is a Gaussian distribution
over the joint space of pixel intensities but rendered tractable through the imposition
of considerable structure reﬂecting the spatial organization of the pixels. Similarly,
the linear dynamical system , used to model time series data for applications suchSection 13.3
as tracking, is also a joint Gaussian distribution over a potentially large number of
observed and latent variables and again is tractable due to the structure imposed on
the distribution. A powerful framework for expressing the form and properties of


## PDF Page 104

2.3. The Gaussian Distribution 85
such complex distributions is that of probabilistic graphical models, which will form
the subject of Chapter 8.
2.3.1 Conditional Gaussian distributions
An important property of the multivariate Gaussian distribution is that if two
sets of variables are jointly Gaussian, then the conditional distribution of one set
conditioned on the other is again Gaussian. Similarly, the marginal distribution of
either set is also Gaussian.
Consider ﬁrst the case of conditional distributions. Supposex is aD-dimensional
vector with Gaussian distribution N(x|µ,Σ) and that we partition x into two dis-
joint subsets xa and xb. Without loss of generality, we can take xa to form the ﬁrst
M components of x, with xb comprising the remaining D − M components, so that
x =
(
xa
xb
)
. (2.65)
We also deﬁne corresponding partitions of the mean vector µ given by
µ =
(
µa
µb
)
(2.66)
and of the covariance matrix Σ given by
Σ =
(
Σaa Σab
Σba Σbb
)
. (2.67)
Note that the symmetry ΣT = Σ of the covariance matrix implies thatΣaa and Σbb
are symmetric, while Σba = ΣT
ab.
In many situations, it will be convenient to work with the inverse of the covari-
ance matrix
Λ ≡ Σ−1 (2.68)
which is known as the precision matrix. In fact, we shall see that some properties
of Gaussian distributions are most naturally expressed in terms of the covariance,
whereas others take a simpler form when viewed in terms of the precision. We
therefore also introduce the partitioned form of the precision matrix
Λ =
(
Λaa Λab
Λba Λbb
)
(2.69)
corresponding to the partitioning (2.65) of the vector x. Because the inverse of a
symmetric matrix is also symmetric, we see that Λaa and Λbb are symmetric, whileExercise 2.22
ΛT
ab = Λba. It should be stressed at this point that, for instance, Λaa is not simply
given by the inverse of Σaa. In fact, we shall shortly examine the relation between
the inverse of a partitioned matrix and the inverses of its partitions.
Let us begin by ﬁnding an expression for the conditional distribution p(xa|xb).
From the product rule of probability, we see that this conditional distribution can be


## PDF Page 105

86 2. PROBABILITY DISTRIBUTIONS
evaluated from the joint distribution p(x)= p(xa,xb) simply by ﬁxing xb to the
observed value and normalizing the resulting expression to obtain a valid probability
distribution over xa. Instead of performing this normalization explicitly, we can
obtain the solution more efﬁciently by considering the quadratic form in the exponent
of the Gaussian distribution given by (2.44) and then reinstating the normalization
coefﬁcient at the end of the calculation. If we make use of the partitioning (2.65),
(2.66), and (2.69), we obtain
− 1
2(x − µ)TΣ−1(x − µ)=
− 1
2(xa − µa)TΛaa(xa − µa) − 1
2(xa − µa)TΛab(xb − µb)
− 1
2(xb − µb)TΛba(xa − µa) − 1
2(xb − µb)TΛbb(xb − µb). (2.70)
We see that as a function of xa, this is again a quadratic form, and hence the cor-
responding conditional distribution p(xa|xb) will be Gaussian. Because this distri-
bution is completely characterized by its mean and its covariance, our goal will be
to identify expressions for the mean and covariance of p(xa|xb) by inspection of
(2.70).
This is an example of a rather common operation associated with Gaussian
distributions, sometimes called ‘completing the square’, in which we are given a
quadratic form deﬁning the exponent terms in a Gaussian distribution, and we need
to determine the corresponding mean and covariance. Such problems can be solved
straightforwardly by noting that the exponent in a general Gaussian distribution
N(x|µ,Σ) can be written
− 1
2(x − µ)TΣ−1(x − µ)=− 1
2xTΣ−1x + xTΣ−1µ +c o n s t (2.71)
where ‘const’ denotes terms which are independent of x, and we have made use of
the symmetry of Σ. Thus if we take our general quadratic form and express it in
the form given by the right-hand side of (2.71), then we can immediately equate the
matrix of coefﬁcients entering the second order term in x to the inverse covariance
matrix Σ
−1 and the coefﬁcient of the linear term in x to Σ−1µ, from which we can
obtain µ.
Now let us apply this procedure to the conditional Gaussian distributionp(xa|xb)
for which the quadratic form in the exponent is given by (2.70). We will denote the
mean and covariance of this distribution by µa|b and Σa|b, respectively. Consider
the functional dependence of (2.70) on xa in which xb is regarded as a constant. If
we pick out all terms that are second order in xa,w eh a v e
− 1
2xT
a Λaaxa (2.72)
from which we can immediately conclude that the covariance (inverse precision) of
p(x
a|xb) is given by
Σa|b = Λ−1
aa . (2.73)


## PDF Page 106

2.3. The Gaussian Distribution 87
Now consider all of the terms in (2.70) that are linear in xa
xT
a {Λaaµa − Λab(xb − µb)} (2.74)
where we have used ΛT
ba = Λab. From our discussion of the general form (2.71),
the coefﬁcient of xa in this expression must equal Σ−1
a|bµa|b and hence
µa|b = Σa|b {Λaaµa − Λab(xb − µb)}
= µa − Λ−1
aa Λab(xb − µb) (2.75)
where we have made use of (2.73).
The results (2.73) and (2.75) are expressed in terms of the partitioned precision
matrix of the original joint distribution p(xa,xb). We can also express these results
in terms of the corresponding partitioned covariance matrix. To do this, we make use
of the following identity for the inverse of a partitioned matrixExercise 2.24
(
AB
CD
)−1
=
(
M −MBD−1
−D−1CM D −1 + D−1CMBD−1
)
(2.76)
where we have deﬁned
M =( A − BD−1C)−1. (2.77)
The quantity M−1 is known as the Schur complement of the matrix on the left-hand
side of (2.76) with respect to the submatrix D. Using the deﬁnition
(
Σaa Σab
Σba Σbb
)−1
=
(
Λaa Λab
Λba Λbb
)
(2.78)
and making use of (2.76), we have
Λaa =( Σaa − ΣabΣ−1
bb Σba)−1 (2.79)
Λab = −(Σaa − ΣabΣ−1
bb Σba)−1ΣabΣ−1
bb . (2.80)
From these we obtain the following expressions for the mean and covariance of the
conditional distribution p(xa|xb)
µa|b = µa + ΣabΣ−1
bb (xb − µb) (2.81)
Σa|b = Σaa − ΣabΣ−1
bb Σba. (2.82)
Comparing (2.73) and (2.82), we see that the conditional distributionp(xa|xb) takes
a simpler form when expressed in terms of the partitioned precision matrix than
when it is expressed in terms of the partitioned covariance matrix. Note that the
mean of the conditional distributionp(xa|xb), given by (2.81), is a linear function of
xb and that the covariance, given by (2.82), is independent ofxa. This represents an
example of a linear-Gaussian model.Section 8.1.4


## PDF Page 107

88 2. PROBABILITY DISTRIBUTIONS
2.3.2 Marginal Gaussian distributions
We have seen that if a joint distribution p(xa,xb) is Gaussian, then the condi-
tional distribution p(xa|xb) will again be Gaussian. Now we turn to a discussion of
the marginal distribution given by
p(xa)=
∫
p(xa,xb)dxb (2.83)
which, as we shall see, is also Gaussian. Once again, our strategy for evaluating this
distribution efﬁciently will be to focus on the quadratic form in the exponent of the
joint distribution and thereby to identify the mean and covariance of the marginal
distribution p(xa).
The quadratic form for the joint distribution can be expressed, using the par-
titioned precision matrix, in the form (2.70). Because our goal is to integrate out
x
b, this is most easily achieved by ﬁrst considering the terms involving xb and then
completing the square in order to facilitate integration. Picking out just those terms
that involvexb,w eh a v e
− 1
2xT
b Λbbxb+xT
b m = − 1
2(xb −Λ−1
bb m)TΛbb(xb −Λ−1
bb m)+ 1
2mTΛ−1
bb m (2.84)
where we have deﬁned
m = Λbbµb − Λba(xa − µa). (2.85)
We see that the dependence onxb has been cast into the standard quadratic form of a
Gaussian distribution corresponding to the ﬁrst term on the right-hand side of (2.84),
plus a term that does not depend on xb (but that does depend on xa). Thus, when
we take the exponential of this quadratic form, we see that the integration over xb
required by (2.83) will take the form
∫
exp
{
− 1
2(xb − Λ−1
bb m)TΛbb(xb − Λ−1
bb m)
}
dxb. (2.86)
This integration is easily performed by noting that it is the integral over an unnor-
malized Gaussian, and so the result will be the reciprocal of the normalization co-
efﬁcient. We know from the form of the normalized Gaussian given by (2.43), that
this coefﬁcient is independent of the mean and depends only on the determinant of
the covariance matrix. Thus, by completing the square with respect to x
b, we can
integrate out xb and the only term remaining from the contributions on the left-hand
side of (2.84) that depends on xa is the last term on the right-hand side of (2.84) in
which m is given by (2.85). Combining this term with the remaining terms from


## PDF Page 108

2.3. The Gaussian Distribution 89
(2.70) that depend on xa, we obtain
1
2 [Λbbµb − Λba(xa − µa)]T Λ−1
bb [Λbbµb − Λba(xa − µa)]
− 1
2xT
a Λaaxa + xT
a (Λaaµa + Λabµb)+c o n s t
= − 1
2xT
a (Λaa − ΛabΛ−1
bb Λba)xa
+xT
a (Λaa − ΛabΛ−1
bb Λba)−1µa +c o n s t (2.87)
where ‘const’ denotes quantities independent of xa. Again, by comparison with
(2.71), we see that the covariance of the marginal distribution of p(xa) is given by
Σa =( Λaa − ΛabΛ−1
bb Λba)−1. (2.88)
Similarly, the mean is given by
Σa(Λaa − ΛabΛ−1
bb Λba)µa = µa (2.89)
where we have used (2.88). The covariance in (2.88) is expressed in terms of the
partitioned precision matrix given by (2.69). We can rewrite this in terms of the
corresponding partitioning of the covariance matrix given by (2.67), as we did for
the conditional distribution. These partitioned matrices are related by
(
Λaa Λab
Λba Λbb
)−1
=
(
Σaa Σab
Σba Σbb
)
(2.90)
Making use of (2.76), we then have
(
Λaa − ΛabΛ−1
bb Λba
)−1
= Σaa. (2.91)
Thus we obtain the intuitively satisfying result that the marginal distribution p(xa)
has mean and covariance given by
E[xa]= µa (2.92)
cov[xa]= Σaa. (2.93)
We see that for a marginal distribution, the mean and covariance are most simply ex-
pressed in terms of the partitioned covariance matrix, in contrast to the conditional
distribution for which the partitioned precision matrix gives rise to simpler expres-
sions.
Our results for the marginal and conditional distributions of a partitioned Gaus-
sian are summarized below.
Partitioned Gaussians
Given a joint Gaussian distribution N(x|µ,Σ) with Λ ≡ Σ−1 and
x =
(
xa
xb
)
, µ =
(
µa
µb
)
(2.94)


## PDF Page 109

90 2. PROBABILITY DISTRIBUTIONS
xa
xb =0 .7
xb
p(xa,xb)
0 0.5 1
0
0.5
1
xa
p(xa)
p(xa|xb =0 .7)
0 0.5 1
0
5
10
Figure 2.9 The plot on the left shows the contours of a Gaussian distribution p(xa,x b) over two variables, and
the plot on the right shows the marginal distribution p(xa) (blue curve) and the conditional distribution p(xa|xb)
for xb =0 .7 (red curve).
Σ =
(
Σaa Σab
Σba Σbb
)
, Λ =
(
Λaa Λab
Λba Λbb
)
. (2.95)
Conditional distribution:
p(xa|xb)=N (x|µa|b,Λ−1
aa ) (2.96)
µa|b = µa − Λ−1
aa Λab(xb − µb). (2.97)
Marginal distribution:
p(xa)=N (xa|µa,Σaa). (2.98)
We illustrate the idea of conditional and marginal distributions associated with
a multivariate Gaussian using an example involving two variables in Figure 2.9.
2.3.3 Bayes’ theorem for Gaussian variables
In Sections 2.3.1 and 2.3.2, we considered a Gaussian p(x) in which we parti-
tioned the vector x into two subvectorsx =( xa,xb) and then found expressions for
the conditional distribution p(xa|xb) and the marginal distribution p(xa). We noted
that the mean of the conditional distribution p(xa|xb) was a linear function of xb.
Here we shall suppose that we are given a Gaussian marginal distributionp(x) and a
Gaussian conditional distribution p(y|x) in which p(y|x) has a mean that is a linear
function of x, and a covariance which is independent of x. This is an example of


## PDF Page 110

2.3. The Gaussian Distribution 91
a linear Gaussian model (Roweis and Ghahramani, 1999), which we shall study in
greater generality in Section 8.1.4. We wish to ﬁnd the marginal distribution p(y)
and the conditional distribution p(x|y). This is a problem that will arise frequently
in subsequent chapters, and it will prove convenient to derive the general results here.
We shall take the marginal and conditional distributions to be
p(x)=N
(
x|µ,Λ−1)
(2.99)
p(y|x)=N
(
y|Ax + b,L−1)
(2.100)
where µ, A, and b are parameters governing the means, and Λ and L are precision
matrices. If x has dimensionality M and y has dimensionality D, then the matrix A
has size D × M.
First we ﬁnd an expression for the joint distribution over x and y. To do this, we
deﬁne
z =
(
x
y
)
(2.101)
and then consider the log of the joint distribution
ln p(z)=l n p(x)+l n p(y|x)
= − 1
2(x − µ)TΛ(x − µ)
− 1
2(y − Ax − b)TL(y − Ax − b) + const (2.102)
where ‘const’ denotes terms independent ofx and y. As before, we see that this is a
quadratic function of the components of z, and hence p(z) is Gaussian distribution.
To ﬁnd the precision of this Gaussian, we consider the second order terms in (2.102),
which can be written as
− 1
2xT(Λ + ATLA)x − 1
2yTLy + 1
2yTLAx + 1
2xTATLy
= − 1
2
(
x
y
)T (
Λ + ATLA −ATL
−LA L
)(
x
y
)
= − 1
2zTRz (2.103)
and so the Gaussian distribution over z has precision (inverse covariance) matrix
given by
R =
(
Λ + ATLA −ATL
−LA L
)
. (2.104)
The covariance matrix is found by taking the inverse of the precision, which can be
done using the matrix inversion formula (2.76) to giveExercise 2.29
cov[z]= R
−1 =
(
Λ−1 Λ−1AT
AΛ−1 L−1 + AΛ−1AT
)
. (2.105)


## PDF Page 111

92 2. PROBABILITY DISTRIBUTIONS
Similarly, we can ﬁnd the mean of the Gaussian distribution over z by identify-
ing the linear terms in (2.102), which are given by
xTΛµ − xTATLb + yTLb =
(
x
y
)T (
Λµ − ATLb
Lb
)
. (2.106)
Using our earlier result (2.71) obtained by completing the square over the quadratic
form of a multivariate Gaussian, we ﬁnd that the mean of z is given by
E[z]=R −1
(
Λµ − ATLb
Lb
)
. (2.107)
Making use of (2.105), we then obtainExercise 2.30
E[z]=
(
µ
Aµ + b
)
. (2.108)
Next we ﬁnd an expression for the marginal distribution p(y) in which we have
marginalized over x. Recall that the marginal distribution over a subset of the com-
ponents of a Gaussian random vector takes a particularly simple form when ex-
pressed in terms of the partitioned covariance matrix. Speciﬁcally, its mean andSection 2.3
covariance are given by (2.92) and (2.93), respectively. Making use of (2.105) and
(2.108) we see that the mean and covariance of the marginal distribution p(y) are
given by
E[y]=A µ + b (2.109)
cov[y]= L
−1 + AΛ−1AT. (2.110)
A special case of this result is when A = I, in which case it reduces to the convolu-
tion of two Gaussians, for which we see that the mean of the convolution is the sum
of the mean of the two Gaussians, and the covariance of the convolution is the sum
of their covariances.
Finally, we seek an expression for the conditionalp(x|y). Recall that the results
for the conditional distribution are most easily expressed in terms of the partitioned
precision matrix, using (2.73) and (2.75). Applying these results to (2.105) andSection 2.3
(2.108) we see that the conditional distribution p(x|y) has mean and covariance
given by
E[x|y]=( Λ + A
TLA)−1 {
ATL(y − b)+ Λµ
}
(2.111)
cov[x|y]=( Λ + ATLA)−1. (2.112)
The evaluation of this conditional can be seen as an example of Bayes’ theorem.
We can interpret the distribution p(x) as a prior distribution over x. If the variable
y is observed, then the conditional distribution p(x|y) represents the corresponding
posterior distribution over x. Having found the marginal and conditional distribu-
tions, we effectively expressed the joint distribution p(z)=p(x)p(y |x) in the form
p(x|y)p(y). These results are summarized below.


## PDF Page 112

2.3. The Gaussian Distribution 93
Marginal and Conditional Gaussians
Given a marginal Gaussian distribution for x and a conditional Gaussian distri-
bution for y given x in the form
p(x)=N (x|µ,Λ−1) (2.113)
p(y|x)=N (y|Ax + b,L−1) (2.114)
the marginal distribution of y and the conditional distribution of x given y are
given by
p(y)=N (y|Aµ + b,L−1 + AΛ−1AT) (2.115)
p(x|y)=N (x|Σ{ATL(y − b)+Λ µ},Σ) (2.116)
where
Σ =( Λ + ATLA)−1. (2.117)
2.3.4 Maximum likelihood for the Gaussian
Given a data set X =( x1,..., xN )T in which the observations {xn} are as-
sumed to be drawn independently from a multivariate Gaussian distribution, we can
estimate the parameters of the distribution by maximum likelihood. The log likeli-
hood function is given by
lnp(X|µ,Σ)=− ND
2 ln(2π)− N
2 ln |Σ|− 1
2
N∑
n=1
(xn−µ)TΣ−1(xn−µ). (2.118)
By simple rearrangement, we see that the likelihood function depends on the data set
only through the two quantities
N∑
n=1
xn,
N∑
n=1
xnxT
n. (2.119)
These are known as the sufﬁcient statistics for the Gaussian distribution. Using
(C.19), the derivative of the log likelihood with respect toµ is given byAppendix C
∂
∂µ ln p(X|µ,Σ)=
N∑
n=1
Σ−1(xn − µ) (2.120)
and setting this derivative to zero, we obtain the solution for the maximum likelihood
estimate of the mean given by
µ
ML = 1
N
N∑
n=1
xn (2.121)


## PDF Page 113

94 2. PROBABILITY DISTRIBUTIONS
which is the mean of the observed set of data points. The maximization of (2.118)
with respect to Σ is rather more involved. The simplest approach is to ignore the
symmetry constraint and show that the resulting solution is symmetric as required.Exercise 2.34
Alternative derivations of this result, which impose the symmetry and positive deﬁ-
niteness constraints explicitly, can be found in Magnus and Neudecker (1999). The
result is as expected and takes the form
Σ
ML = 1
N
N∑
n=1
(xn − µML)(xn − µML)T (2.122)
which involves µML because this is the result of a joint maximization with respect
to µ and Σ. Note that the solution (2.121) for µML does not depend onΣML, and so
we can ﬁrst evaluate µML and then use this to evaluate ΣML.
If we evaluate the expectations of the maximum likelihood solutions under the
true distribution, we obtain the following resultsExercise 2.35
E[µML]= µ (2.123)
E[ΣML]= N − 1
N Σ. (2.124)
We see that the expectation of the maximum likelihood estimate for the mean is equal
to the true mean. However, the maximum likelihood estimate for the covariance has
an expectation that is less than the true value, and hence it is biased. We can correct
this bias by deﬁning a different estimator
˜Σ given by
˜Σ = 1
N − 1
N∑
n=1
(xn − µML)(xn − µML)T. (2.125)
Clearly from (2.122) and (2.124), the expectation of ˜Σ is equal to Σ.
2.3.5 Sequential estimation
Our discussion of the maximum likelihood solution for the parameters of a Gaus-
sian distribution provides a convenient opportunity to give a more general discussion
of the topic of sequential estimation for maximum likelihood. Sequential methods
allow data points to be processed one at a time and then discarded and are important
for on-line applications, and also where large data sets are involved so that batch
processing of all data points at once is infeasible.
Consider the result (2.121) for the maximum likelihood estimator of the mean
µML, which we will denote by µ(N)
ML when it is based on N observations. If we


## PDF Page 114

2.3. The Gaussian Distribution 95
Figure 2.10 A schematic illustration of two correlated ran-
dom variables z and θ, together with the
regression function f(θ) given by the con-
ditional expectation E[z|θ]. The Robbins-
Monro algorithm provides a general sequen-
tial procedure for ﬁnding the root θ
⋆ of such
functions. θ
z
θ⋆
f(θ)
dissect out the contribution from the ﬁnal data point xN , we obtain
µ(N)
ML = 1
N
N∑
n=1
xn
= 1
N xN + 1
N
N −1∑
n=1
xn
= 1
N xN + N − 1
N µ(N −1)
ML
= µ(N −1)
ML + 1
N (xN − µ(N −1)
ML ). (2.126)
This result has a nice interpretation, as follows. After observing N − 1 data points
we have estimated µ by µ(N −1)
ML . We now observe data pointxN , and we obtain our
revised estimate µ(N)
ML by moving the old estimate a small amount, proportional to
1/N, in the direction of the ‘error signal’(xN − µ(N −1)
ML ). Note that, as N increases,
so the contribution from successive data points gets smaller.
The result (2.126) will clearly give the same answer as the batch result (2.121)
because the two formulae are equivalent. However, we will not always be able to de-
rive a sequential algorithm by this route, and so we seek a more general formulation
of sequential learning, which leads us to the Robbins-Monro algorithm. Consider a
pair of random variables θand z governed by a joint distribution p(z,θ). The con-
ditional expectation of z given θ deﬁnes a deterministic function f(θ) that is given
by
f(θ) ≡ E[z|θ]=
∫
zp(z|θ)d z (2.127)
and is illustrated schematically in Figure 2.10. Functions deﬁned in this way are
called regression functions.
Our goal is to ﬁnd the root θ⋆ at which f(θ⋆)=0 . If we had a large data set
of observations of z and θ, then we could model the regression function directly and
then obtain an estimate of its root. Suppose, however, that we observe values of
z one at a time and we wish to ﬁnd a corresponding sequential estimation scheme
for θ
⋆. The following general procedure for solving such problems was given by


## PDF Page 115

96 2. PROBABILITY DISTRIBUTIONS
Robbins and Monro (1951). We shall assume that the conditional variance of z is
ﬁnite so that
E
[
(z − f)2 |θ
]
< ∞ (2.128)
and we shall also, without loss of generality, consider the case where f(θ) > 0 for
θ>θ ⋆ and f(θ) < 0 for θ<θ ⋆, as is the case in Figure 2.10. The Robbins-Monro
procedure then deﬁnes a sequence of successive estimates of the root θ⋆ given by
θ(N) = θ(N −1) + aN −1z(θ(N −1)) (2.129)
where z(θ(N)) is an observed value ofz when θtakes the valueθ(N). The coefﬁcients
{aN } represent a sequence of positive numbers that satisfy the conditions
lim
N →∞
aN =0 (2.130)
∞∑
N=1
aN = ∞ (2.131)
∞∑
N=1
a2
N < ∞. (2.132)
It can then be shown (Robbins and Monro, 1951; Fukunaga, 1990) that the sequence
of estimates given by (2.129) does indeed converge to the root with probability one.
Note that the ﬁrst condition (2.130) ensures that the successive corrections decrease
in magnitude so that the process can converge to a limiting value. The second con-
dition (2.131) is required to ensure that the algorithm does not converge short of the
root, and the third condition (2.132) is needed to ensure that the accumulated noise
has ﬁnite variance and hence does not spoil convergence.
Now let us consider how a general maximum likelihood problem can be solved
sequentially using the Robbins-Monro algorithm. By deﬁnition, the maximum like-
lihood solution θ
ML is a stationary point of the log likelihood function and hence
satisﬁes
∂
∂θ
{
1
N
N∑
n=1
lnp(xn|θ)
} ⏐⏐
⏐⏐⏐
θML
=0 . (2.133)
Exchanging the derivative and the summation, and taking the limitN →∞ we have
lim
N →∞
1
N
N∑
n=1
∂
∂θlnp(xn|θ)=E x
[ ∂
∂θlnp(x|θ)
]
(2.134)
and so we see that ﬁnding the maximum likelihood solution corresponds to ﬁnd-
ing the root of a regression function. We can therefore apply the Robbins-Monro
procedure, which now takes the form
θ
(N) = θ(N −1) + aN −1
∂
∂θ(N −1) ln p(xN |θ(N −1)). (2.135)


## PDF Page 116

2.3. The Gaussian Distribution 97
Figure 2.11 In the case of a Gaussian distribution, with θ
corresponding to the mean µ, the regression
function illustrated in Figure 2.10 takes the form
of a straight line, as shown in red. In this
case, the random variable z corresponds to the
derivative of the log likelihood function and is
given by (x − µ
ML)/σ2, and its expectation that
deﬁnes the regression function is a straight line
given by (µ − µML)/σ2. The root of the regres-
sion function corresponds to the maximum like-
lihood estimator µ
ML.
µ
z
p(z|µ)
µML
As a speciﬁc example, we consider once again the sequential estimation of the
mean of a Gaussian distribution, in which case the parameter θ(N) is the estimate
µ(N)
ML of the mean of the Gaussian, and the random variable z is given by
z = ∂
∂µML
lnp(x|µML,σ2)= 1
σ2 (x − µML). (2.136)
Thus the distribution of z is Gaussian with mean µ − µML, as illustrated in Fig-
ure 2.11. Substituting (2.136) into (2.135), we obtain the univariate form of (2.126),
provided we choose the coefﬁcients aN to have the form aN = σ2/N. Note that
although we have focussed on the case of a single variable, the same technique,
together with the same restrictions (2.130)–(2.132) on the coefﬁcients aN , apply
equally to the multivariate case (Blum, 1965).
2.3.6 Bayesian inference for the Gaussian
The maximum likelihood framework gave point estimates for the parameters µ
and Σ. Now we develop a Bayesian treatment by introducing prior distributions
over these parameters. Let us begin with a simple example in which we consider a
single Gaussian random variable x. We shall suppose that the variance σ
2 is known,
and we consider the task of inferring the mean µ given a set of N observations
X = {x1,...,x N }. The likelihood function, that is the probability of the observed
data given µ, viewed as a function of µ,i sg i v e nb y
p(X|µ)=
N∏
n=1
p(xn|µ)= 1
(2πσ2)N/2 exp
{
− 1
2σ2
N∑
n=1
(xn − µ)2
}
. (2.137)
Again we emphasize that the likelihood function p(X|µ) is not a probability distri-
bution over µ and is not normalized.
We see that the likelihood function takes the form of the exponential of a quad-
ratic form in µ. Thus if we choose a prior p(µ) given by a Gaussian, it will be a


## PDF Page 117

98 2. PROBABILITY DISTRIBUTIONS
conjugate distribution for this likelihood function because the corresponding poste-
rior will be a product of two exponentials of quadratic functions of µ and hence will
also be Gaussian. We therefore take our prior distribution to be
p(µ)=N
(
µ|µ0,σ2
0
)
(2.138)
and the posterior distribution is given by
p(µ|X) ∝ p(X|µ)p(µ). (2.139)
Simple manipulation involving completing the square in the exponent shows that theExercise 2.38
posterior distribution is given by
p(µ|X)=N
(
µ|µN ,σ2
N
)
(2.140)
where
µN = σ2
Nσ2
0 + σ2 µ0 + Nσ2
0
Nσ2
0 + σ2 µML (2.141)
1
σ2
N
= 1
σ2
0
+ N
σ2 (2.142)
in which µML is the maximum likelihood solution for µ given by the sample mean
µML = 1
N
N∑
n=1
xn. (2.143)
It is worth spending a moment studying the form of the posterior mean and
variance. First of all, we note that the mean of the posterior distribution given by
(2.141) is a compromise between the prior mean µ0 and the maximum likelihood
solution µML. If the number of observed data points N =0 , then (2.141) reduces
to the prior mean as expected. For N →∞ , the posterior mean is given by the
maximum likelihood solution. Similarly, consider the result (2.142) for the variance
of the posterior distribution. We see that this is most naturally expressed in terms
of the inverse variance, which is called the precision. Furthermore, the precisions
are additive, so that the precision of the posterior is given by the precision of the
prior plus one contribution of the data precision from each of the observed data
points. As we increase the number of observed data points, the precision steadily
increases, corresponding to a posterior distribution with steadily decreasing variance.
With no observed data points, we have the prior variance, whereas if the number of
data points N →∞ , the variance σ
2
N goes to zero and the posterior distribution
becomes inﬁnitely peaked around the maximum likelihood solution. We therefore
see that the maximum likelihood result of a point estimate for µ given by (2.143) is
recovered precisely from the Bayesian formalism in the limit of an inﬁnite number
of observations. Note also that for ﬁnite N, if we take the limitσ
2
0 →∞ in which the
prior has inﬁnite variance then the posterior mean (2.141) reduces to the maximum
likelihood result, while from (2.142) the posterior variance is given byσ2
N = σ2/N.


## PDF Page 118

2.3. The Gaussian Distribution 99
Figure 2.12 Illustration of Bayesian inference for
the mean µ of a Gaussian distri-
bution, in which the variance is as-
sumed to be known. The curves
show the prior distribution over µ
(the curve labelled N =0 ), which
in this case is itself Gaussian, along
with the posterior distribution given
by (2.140) for increasing numbers N
of data points. The data points are
generated from a Gaussian of mean
0.8 and variance 0.1, and the prior is
chosen to have mean 0. In both the
prior and the likelihood function, the
variance is set to the true value.
N =0
N =1
N =2
N =1 0
−1 0 1
0
5
We illustrate our analysis of Bayesian inference for the mean of a Gaussian
distribution in Figure 2.12. The generalization of this result to the case of a D-
dimensional Gaussian random variablex with known covariance and unknown mean
is straightforward.Exercise 2.40
We have already seen how the maximum likelihood expression for the mean of
a Gaussian can be re-cast as a sequential update formula in which the mean afterSection 2.3.5
observing N data points was expressed in terms of the mean after observing N − 1
data points together with the contribution from data point xN . In fact, the Bayesian
paradigm leads very naturally to a sequential view of the inference problem. To see
this in the context of the inference of the mean of a Gaussian, we write the posterior
distribution with the contribution from the ﬁnal data point xN separated out so that
p(µ|D) ∝
[
p(µ)
N −1∏
n=1
p(xn|µ)
]
p(xN |µ). (2.144)
The term in square brackets is (up to a normalization coefﬁcient) just the posterior
distribution after observing N − 1 data points. We see that this can be viewed as
a prior distribution, which is combined using Bayes’ theorem with the likelihood
function associated with data point xN to arrive at the posterior distribution after
observing N data points. This sequential view of Bayesian inference is very general
and applies to any problem in which the observed data are assumed to be independent
and identically distributed.
So far, we have assumed that the variance of the Gaussian distribution over the
data is known and our goal is to infer the mean. Now let us suppose that the mean
is known and we wish to infer the variance. Again, our calculations will be greatly
simpliﬁed if we choose a conjugate form for the prior distribution. It turns out to be
most convenient to work with the precisionλ ≡ 1/σ
2. The likelihood function for λ
takes the form
p(X|λ)=
N∏
n=1
N(xn|µ, λ−1) ∝ λN/2 exp
{
− λ
2
N∑
n=1
(xn − µ)2
}
. (2.145)


## PDF Page 119

100 2. PROBABILITY DISTRIBUTIONS
λ
a =0 .1
b =0 .1
0 1 2
0
1
2
λ
a =1
b =1
0 1 2
0
1
2
λ
a =4
b =6
0 1 2
0
1
2
Figure 2.13 Plot of the gamma distributionGam(λ|a, b) deﬁned by (2.146) for various values of the parameters
a and b.
The corresponding conjugate prior should therefore be proportional to the product
of a power of λ and the exponential of a linear function of λ. This corresponds to
the gamma distribution which is deﬁned by
Gam(λ|a, b)= 1
Γ(a)baλa−1 exp(−bλ). (2.146)
Here Γ(a) is the gamma function that is deﬁned by (1.141) and that ensures that
(2.146) is correctly normalized. The gamma distribution has a ﬁnite integral ifa> 0,Exercise 2.41
and the distribution itself is ﬁnite if a ⩾ 1. It is plotted, for various values of a and
b, in Figure 2.13. The mean and variance of the gamma distribution are given byExercise 2.42
E[λ]= a
b (2.147)
var[λ]= a
b2 . (2.148)
Consider a prior distribution Gam(λ|a0,b0). If we multiply by the likelihood
function (2.145), then we obtain a posterior distribution
p(λ|X) ∝ λa0−1λN/2 exp
{
−b0λ − λ
2
N∑
n=1
(xn − µ)2
}
(2.149)
which we recognize as a gamma distribution of the form Gam(λ|aN ,b N ) where
aN = a0 + N
2 (2.150)
bN = b0 + 1
2
N∑
n=1
(xn − µ)2 = b0 + N
2 σ2
ML (2.151)
where σ2
ML is the maximum likelihood estimator of the variance. Note that in (2.149)
there is no need to keep track of the normalization constants in the prior and the
likelihood function because, if required, the correct coefﬁcient can be found at the
end using the normalized form (2.146) for the gamma distribution.


## PDF Page 120

2.3. The Gaussian Distribution 101
From (2.150), we see that the effect of observing N data points is to increase
the value of the coefﬁcient a by N/2. Thus we can interpret the parameter a0 in
the prior in terms of 2a0 ‘effective’ prior observations. Similarly, from (2.151) we
see that the N data points contribute Nσ2
ML/2 to the parameter b, where σ2
ML is
the variance, and so we can interpret the parameter b0 in the prior as arising from
the 2a0 ‘effective’ prior observations having variance 2b0/(2a0)=b 0/a0. Recall
that we made an analogous interpretation for the Dirichlet prior. These distributionsSection 2.2
are examples of the exponential family, and we shall see that the interpretation of
a conjugate prior in terms of effective ﬁctitious data points is a general one for the
exponential family of distributions.
Instead of working with the precision, we can consider the variance itself. The
conjugate prior in this case is called the inverse gamma distribution, although we
shall not discuss this further because we will ﬁnd it more convenient to work with
the precision.
Now suppose that both the mean and the precision are unknown. To ﬁnd a
conjugate prior, we consider the dependence of the likelihood function on µ and λ
p(X|µ, λ)=
N∏
n=1
( λ
2π
)1/2
exp
{
− λ
2(xn − µ)2
}
∝
[
λ1/2 exp
(
− λµ2
2
)]N
exp
{
λµ
N∑
n=1
xn − λ
2
N∑
n=1
x2
n
}
. (2.152)
We now wish to identify a prior distribution p(µ, λ) that has the same functional
dependence on µ and λ as the likelihood function and that should therefore take the
form
p(µ, λ) ∝
[
λ1/2 exp
(
− λµ2
2
)]β
exp {cλµ − dλ}
=e x p
{
− βλ
2 (µ − c/β)2
}
λβ/2 exp
{
−
(
d − c2
2β
)
λ
}
(2.153)
where c, d, and β are constants. Since we can always write p(µ, λ)= p(µ|λ)p(λ),
we can ﬁnd p(µ|λ) and p(λ) by inspection. In particular, we see that p(µ|λ) is a
Gaussian whose precision is a linear function of λ and that p(λ) is a gamma distri-
bution, so that the normalized prior takes the form
p(µ, λ)=N (µ|µ0, (βλ)−1)Gam(λ|a, b) (2.154)
where we have deﬁned new constants given by µ0 = c/β, a =1 + β/2, b =
d−c2/2β. The distribution (2.154) is called thenormal-gamma or Gaussian-gamma
distribution and is plotted in Figure 2.14. Note that this is not simply the product
of an independent Gaussian prior over µ and a gamma prior over λ, because the
precision of µ is a linear function of λ. Even if we chose a prior in which µ and λ
were independent, the posterior distribution would exhibit a coupling between the
precision of µ and the value of λ.


## PDF Page 121

102 2. PROBABILITY DISTRIBUTIONS
Figure 2.14 Contour plot of the normal-gamma
distribution (2.154) for parameter
values µ0 =0 , β =2 , a =5 and
b =6 .
µ
λ
−2 0 2
0
1
2
In the case of the multivariate Gaussian distribution N
(
x|µ,Λ−1)
for a D-
dimensional variable x, the conjugate prior distribution for the mean µ, assuming
the precision is known, is again a Gaussian. For known mean and unknown precision
matrix Λ, the conjugate prior is the Wishart distribution given byExercise 2.45
W(Λ|W,ν)=B |Λ|(ν−D−1)/2 exp
(
− 1
2Tr(W−1Λ)
)
(2.155)
where νis called the number ofdegrees of freedom of the distribution,W is a D ×D
scale matrix, and Tr(·) denotes the trace. The normalization constant B is given by
B(W,ν)=|W |−ν/2
(
2νD/2 πD(D−1)/4
D∏
i=1
Γ
(ν+1 − i
2
))−1
. (2.156)
Again, it is also possible to deﬁne a conjugate prior over the covariance matrix itself,
rather than over the precision matrix, which leads to the inverse Wishart distribu-
tion, although we shall not discuss this further. If both the mean and the precision
are unknown, then, following a similar line of reasoning to the univariate case, the
conjugate prior is given by
p(µ,Λ|µ
0,β, W,ν)=N (µ|µ0, (βΛ)−1) W(Λ|W,ν) (2.157)
which is known as the normal-Wishart or Gaussian-Wishart distribution.
2.3.7 Student’s t-distribution
We have seen that the conjugate prior for the precision of a Gaussian is given
by a gamma distribution. If we have a univariate Gaussian N(x|µ, τ−1) togetherSection 2.3.6
with a Gamma prior Gam(τ|a, b) and we integrate out the precision, we obtain the
marginal distribution of x in the formExercise 2.46


## PDF Page 122

2.3. The Gaussian Distribution 103
Figure 2.15 Plot of Student’s t-distribution (2.159)
for µ =0 and λ =1 for various values
of ν. The limit ν →∞ corresponds
to a Gaussian distribution with mean
µ and precision λ.
ν →∞
ν =1 .0
ν =0 .1
−5 0 5
0
0.1
0.2
0.3
0.4
0.5
p(x|µ, a, b)=
∫ ∞
0
N(x|µ, τ−1)Gam(τ|a, b)d τ (2.158)
=
∫ ∞
0
bae(−bτ)τa−1
Γ(a)
( τ
2π
)1/2
exp
{
− τ
2(x − µ)2
}
dτ
= ba
Γ(a)
( 1
2π
)1/2 [
b + (x − µ)2
2
]−a−1/2
Γ(a +1 /2)
where we have made the change of variable z = τ[b +( x − µ)2/2]. By convention
we deﬁne new parameters given by ν =2 a and λ = a/b, in terms of which the
distribution p(x|µ, a, b) takes the form
St(x|µ, λ, ν)= Γ(ν/2+1 /2)
Γ(ν/2)
( λ
πν
)1/2 [
1+ λ(x − µ)2
ν
]−ν/2−1/2
(2.159)
which is known as Student’s t-distribution. The parameter λ is sometimes called the
precision of the t-distribution, even though it is not in general equal to the inverse
of the variance. The parameter ν is called the degrees of freedom, and its effect is
illustrated in Figure 2.15. For the particular case of ν =1 , the t-distribution reduces
to the Cauchy distribution, while in the limit ν →∞ the t-distribution St(x|µ, λ, ν)
becomes a Gaussian N(x|µ, λ−1) with mean µ and precision λ.Exercise 2.47
From (2.158), we see that Student’s t-distribution is obtained by adding up an
inﬁnite number of Gaussian distributions having the same mean but different preci-
sions. This can be interpreted as an inﬁnite mixture of Gaussians (Gaussian mixtures
will be discussed in detail in Section 2.3.9. The result is a distribution that in gen-
eral has longer ‘tails’ than a Gaussian, as was seen in Figure 2.15. This gives the t-
distribution an important property calledrobustness, which means that it is much less
sensitive than the Gaussian to the presence of a few data points which are outliers.
The robustness of the t-distribution is illustrated in Figure 2.16, which compares the
maximum likelihood solutions for a Gaussian and a t-distribution. Note that the max-
imum likelihood solution for the t-distribution can be found using the expectation-
maximization (EM) algorithm. Here we see that the effect of a small number ofExercise 12.24


## PDF Page 123

104 2. PROBABILITY DISTRIBUTIONS
(a)
−5 0 5 10
0
0.1
0.2
0.3
0.4
0.5
(b)
−5 0 5 10
0
0.1
0.2
0.3
0.4
0.5
Figure 2.16 Illustration of the robustness of Student’s t-distribution compared to a Gaussian. (a) Histogram
distribution of 30 data points drawn from a Gaussian distribution, together with the maximum likelihood ﬁt ob-
tained from a t-distribution (red curve) and a Gaussian (green curve, largely hidden by the red curve). Because
the t-distribution contains the Gaussian as a special case it gives almost the same solution as the Gaussian.
(b) The same data set but with three additional outlying data points showing how the Gaussian (green curve) is
strongly distorted by the outliers, whereas the t-distribution (red curve) is relatively unaffected.
outliers is much less signiﬁcant for the t-distribution than for the Gaussian. Outliers
can arise in practical applications either because the process that generates the data
corresponds to a distribution having a heavy tail or simply through mislabelled data.
Robustness is also an important property for regression problems. Unsurprisingly,
the least squares approach to regression does not exhibit robustness, because it cor-
responds to maximum likelihood under a (conditional) Gaussian distribution. By
basing a regression model on a heavy-tailed distribution such as a t-distribution, we
obtain a more robust model.
If we go back to (2.158) and substitute the alternative parameters ν =2 a, λ =
a/b, and η= τb/a, we see that the t-distribution can be written in the form
St(x|µ, λ, ν)=
∫ ∞
0
N
(
x|µ,(ηλ)−1)
Gam(η|ν/2,ν/2) dη. (2.160)
We can then generalize this to a multivariate Gaussian N(x|µ,Λ) to obtain the cor-
responding multivariate Student’s t-distribution in the form
St(x|µ,Λ,ν)=
∫ ∞
0
N(x|µ,(ηΛ)−1)Gam(η|ν/2,ν/2) dη. (2.161)
Using the same technique as for the univariate case, we can evaluate this integral to
giveExercise 2.48


## PDF Page 124

2.3. The Gaussian Distribution 105
St(x|µ,Λ,ν)= Γ(D/2+ ν/2)
Γ(ν/2)
|Λ|1/2
(πν)D/2
[
1+ ∆2
ν
]−D/2−ν/2
(2.162)
where D is the dimensionality of x, and ∆2 is the squared Mahalanobis distance
deﬁned by
∆2 =( x − µ)TΛ(x − µ). (2.163)
This is the multivariate form of Student’s t-distribution and satisﬁes the following
propertiesExercise 2.49
E[x]= µ, if ν> 1 (2.164)
cov[x]= ν
(ν − 2)Λ−1, if ν> 2 (2.165)
mode[x]= µ (2.166)
with corresponding results for the univariate case.
2.3.8 Periodic variables
Although Gaussian distributions are of great practical signiﬁcance, both in their
own right and as building blocks for more complex probabilistic models, there are
situations in which they are inappropriate as density models for continuous vari-
ables. One important case, which arises in practical applications, is that of periodic
variables.
An example of a periodic variable would be the wind direction at a particular
geographical location. We might, for instance, measure values of wind direction on a
number of days and wish to summarize this using a parametric distribution. Another
example is calendar time, where we may be interested in modelling quantities that
are believed to be periodic over 24 hours or over an annual cycle. Such quantities
can conveniently be represented using an angular (polar) coordinate 0 ⩽ θ< 2π.
We might be tempted to treat periodic variables by choosing some direction
as the origin and then applying a conventional distribution such as the Gaussian.
Such an approach, however, would give results that were strongly dependent on the
arbitrary choice of origin. Suppose, for instance, that we have two observations at
θ
1 =1 ◦ and θ2 = 359◦, and we model them using a standard univariate Gaussian
distribution. If we choose the origin at 0◦, then the sample mean of this data set
will be 180◦ with standard deviation 179◦, whereas if we choose the origin at 180◦,
then the mean will be 0◦ and the standard deviation will be 1◦. We clearly need to
develop a special approach for the treatment of periodic variables.
Let us consider the problem of evaluating the mean of a set of observations
D = {θ1,...,θ N } of a periodic variable. From now on, we shall assume that θ is
measured in radians. We have already seen that the simple average(θ1+··· +θN )/N
will be strongly coordinate dependent. To ﬁnd an invariant measure of the mean, we
note that the observations can be viewed as points on the unit circle and can therefore
be described instead by two-dimensional unit vectors x1,..., xN where ∥xn∥ =1
for n =1 ,...,N , as illustrated in Figure 2.17. We can average the vectors {xn}


## PDF Page 125

106 2. PROBABILITY DISTRIBUTIONS
Figure 2.17 Illustration of the representation of val-
ues θn of a periodic variable as two-
dimensional vectors xn living on the unit
circle. Also shown is the average x of
those vectors.
x1
x2
x1
x2
x3x4
¯x
¯r
¯θ
instead to give
x = 1
N
N∑
n=1
xn (2.167)
and then ﬁnd the corresponding angle θof this average. Clearly, this deﬁnition will
ensure that the location of the mean is independent of the origin of the angular coor-
dinate. Note that x will typically lie inside the unit circle. The Cartesian coordinates
of the observations are given by xn =( c o sθn, sinθn), and we can write the Carte-
sian coordinates of the sample mean in the form x =( r cos θ,r sinθ). Substituting
into (2.167) and equating the x1 and x2 components then gives
r cos θ= 1
N
N∑
n=1
cos θn, r sin θ= 1
N
N∑
n=1
sin θn. (2.168)
Taking the ratio, and using the identity tanθ =s i nθ/cos θ, we can solve for θ to
give
θ= tan−1
{ ∑
n sinθn∑
n cos θn
}
. (2.169)
Shortly, we shall see how this result arises naturally as the maximum likelihood
estimator for an appropriately deﬁned distribution over a periodic variable.
We now consider a periodic generalization of the Gaussian called thevon Mises
distribution. Here we shall limit our attention to univariate distributions, although
periodic distributions can also be found over hyperspheres of arbitrary dimension.
For an extensive discussion of periodic distributions, see Mardia and Jupp (2000).
By convention, we will consider distributions p(θ) that have period 2π.A n y
probability density p(θ) deﬁned over θ must not only be nonnegative and integrate


## PDF Page 126

2.3. The Gaussian Distribution 107
Figure 2.18 The von Mises distribution can be derived by considering
a two-dimensional Gaussian of the form (2.173), whose
density contours are shown in blue and conditioning on
the unit circle shown in red.
x1
x2
p(x)
r =1
to one, but it must also be periodic. Thus p(θ) must satisfy the three conditions
p(θ) ⩾ 0 (2.170)
∫ 2π
0
p(θ)d θ =1 (2.171)
p(θ+2 π)=p(θ ). (2.172)
From (2.172), it follows that p(θ+ M2π)=p(θ ) for any integer M.
We can easily obtain a Gaussian-like distribution that satisﬁes these three prop-
erties as follows. Consider a Gaussian distribution over two variables x =( x1,x2)
having mean µ =( µ1,µ2) and a covariance matrix Σ = σ2I where I is the 2 × 2
identity matrix, so that
p(x1,x2)= 1
2πσ2 exp
{
− (x1 − µ1)2 +( x2 − µ2)2
2σ2
}
. (2.173)
The contours of constant p(x) are circles, as illustrated in Figure 2.18. Now suppose
we consider the value of this distribution along a circle of ﬁxed radius. Then by con-
struction this distribution will be periodic, although it will not be normalized. We can
determine the form of this distribution by transforming from Cartesian coordinates
(x1,x2) to polar coordinates (r, θ) so that
x1 = r cos θ, x 2 = r sin θ. (2.174)
We also map the mean µ into polar coordinates by writing
µ1 = r0 cos θ0,µ 2 = r0 sin θ0. (2.175)
Next we substitute these transformations into the two-dimensional Gaussian distribu-
tion (2.173), and then condition on the unit circler =1 , noting that we are interested
only in the dependence on θ. Focussing on the exponent in the Gaussian distribution
we have
− 1
2σ2
{
(r cos θ− r0 cos θ0)2 +( r sin θ− r0 sin θ0)2}
= − 1
2σ2
{
1+ r2
0 − 2r0 cos θcos θ0 − 2r0 sinθsin θ0
}
= r0
σ2 cos(θ− θ0)+c o n s t (2.176)


## PDF Page 127

108 2. PROBABILITY DISTRIBUTIONS
m =5 , θ0 = π/4
m =1 , θ0 =3 π/4
2π
0
π/4
3π/4
m =5 , θ0 = π/4
m =1 , θ0 =3 π/4
Figure 2.19 The von Mises distribution plotted for two different parameter values, shown as a Cartesian plot
on the left and as the corresponding polar plot on the right.
where ‘const’ denotes terms independent ofθ, and we have made use of the following
trigonometrical identitiesExercise 2.51
cos2 A +s i n2 A =1 (2.177)
cos A cos B +s i nA sin B =c o s (A − B). (2.178)
If we now deﬁne m = r0/σ2, we obtain our ﬁnal expression for the distribution of
p(θ) along the unit circle r =1 in the form
p(θ|θ0,m )= 1
2πI0(m) exp {m cos(θ− θ0)} (2.179)
which is called the von Mises distribution, or the circular normal. Here the param-
eter θ0 corresponds to the mean of the distribution, while m, which is known as
the concentration parameter, is analogous to the inverse variance (precision) for the
Gaussian. The normalization coefﬁcient in (2.179) is expressed in terms of I0(m),
which is the zeroth-order Bessel function of the ﬁrst kind (Abramowitz and Stegun,
1965) and is deﬁned by
I0(m)= 1
2π
∫ 2π
0
exp {m cos θ} dθ. (2.180)
For large m, the distribution becomes approximately Gaussian. The von Mises dis-Exercise 2.52
tribution is plotted in Figure 2.19, and the function I0(m) is plotted in Figure 2.20.
Now consider the maximum likelihood estimators for the parameters θ0 and m
for the von Mises distribution. The log likelihood function is given by
lnp(D|θ0,m )=−N ln(2π) − N ln I0(m)+m
N∑
n=1
cos(θn − θ0). (2.181)


## PDF Page 128

2.3. The Gaussian Distribution 109
I0(m)
m
0 5 10
0
1000
2000
3000
A(m)
m
0 5 10
0
0.5
1
Figure 2.20 Plot of the Bessel function I0(m) deﬁned by (2.180), together with the function A(m) deﬁned by
(2.186).
Setting the derivative with respect toθ0 equal to zero gives
N∑
n=1
sin(θn − θ0)=0 . (2.182)
To solve forθ0, we make use of the trigonometric identity
sin(A − B)=c o sB sinA − cos A sinB (2.183)
from which we obtainExercise 2.53
θML
0 = tan−1
{ ∑
n sin θn∑
n cos θn
}
(2.184)
which we recognize as the result (2.169) obtained earlier for the mean of the obser-
vations viewed in a two-dimensional Cartesian space.
Similarly, maximizing (2.181) with respect to m, and making use of I′
0(m)=
I1(m) (Abramowitz and Stegun, 1965), we have
A(m)= 1
N
N∑
n=1
cos(θn − θML
0 ) (2.185)
where we have substituted for the maximum likelihood solution for θML
0 (recalling
that we are performing a joint optimization over θand m), and we have deﬁned
A(m)= I1(m)
I0(m). (2.186)
The function A(m) is plotted in Figure 2.20. Making use of the trigonometric iden-
tity (2.178), we can write (2.185) in the form
A(mML)=
(
1
N
N∑
n=1
cos θn
)
cos θML
0 −
(
1
N
N∑
n=1
sin θn
)
sinθML
0 . (2.187)


## PDF Page 129

110 2. PROBABILITY DISTRIBUTIONS
Figure 2.21 Plots of the ‘old faith-
ful’ data in which the blue curves
show contours of constant proba-
bility density. On the left is a
single Gaussian distribution which
has been ﬁtted to the data us-
ing maximum likelihood. Note that
this distribution fails to capture the
two clumps in the data and indeed
places much of its probability mass
in the central region between the
clumps where the data are relatively
sparse. On the right the distribution
is given by a linear combination of
two Gaussians which has been ﬁtted
to the data by maximum likelihood
using techniques discussed Chap-
ter 9, and which gives a better rep-
resentation of the data.
1 2 3 4 5 6
40
60
80
100
1 2 3 4 5 6
40
60
80
100
The right-hand side of (2.187) is easily evaluated, and the function A(m) can be
inverted numerically.
For completeness, we mention brieﬂy some alternative techniques for the con-
struction of periodic distributions. The simplest approach is to use a histogram of
observations in which the angular coordinate is divided into ﬁxed bins. This has the
virtue of simplicity and ﬂexibility but also suffers from signiﬁcant limitations, as we
shall see when we discuss histogram methods in more detail in Section 2.5. Another
approach starts, like the von Mises distribution, from a Gaussian distribution over a
Euclidean space but now marginalizes onto the unit circle rather than conditioning
(Mardia and Jupp, 2000). However, this leads to more complex forms of distribution
and will not be discussed further. Finally, any valid distribution over the real axis
(such as a Gaussian) can be turned into a periodic distribution by mapping succes-
sive intervals of width 2π onto the periodic variable (0, 2π), which corresponds to
‘wrapping’ the real axis around unit circle. Again, the resulting distribution is more
complex to handle than the von Mises distribution.
One limitation of the von Mises distribution is that it is unimodal. By forming
mixtures of von Mises distributions, we obtain a ﬂexible framework for modelling
periodic variables that can handle multimodality. For an example of a machine learn-
ing application that makes use of von Mises distributions, see Lawrenceet al. (2002),
and for extensions to modelling conditional densities for regression problems, see
Bishop and Nabney (1996).
2.3.9 Mixtures of Gaussians
While the Gaussian distribution has some important analytical properties, it suf-
fers from signiﬁcant limitations when it comes to modelling real data sets. Consider
the example shown in Figure 2.21. This is known as the ‘Old Faithful’ data set,
and comprises 272 measurements of the eruption of the Old Faithful geyser at Yel-
lowstone National Park in the USA. Each measurement comprises the duration ofAppendix A


## PDF Page 130

2.3. The Gaussian Distribution 111
Figure 2.22 Example of a Gaussian mixture distribution
in one dimension showing three Gaussians
(each scaled by a coefﬁcient) in blue and
their sum in red.
x
p(x)
the eruption in minutes (horizontal axis) and the time in minutes to the next erup-
tion (vertical axis). We see that the data set forms two dominant clumps, and that
a simple Gaussian distribution is unable to capture this structure, whereas a linear
superposition of two Gaussians gives a better characterization of the data set.
Such superpositions, formed by taking linear combinations of more basic dis-
tributions such as Gaussians, can be formulated as probabilistic models known as
mixture distributions (McLachlan and Basford, 1988; McLachlan and Peel, 2000).
In Figure 2.22 we see that a linear combination of Gaussians can give rise to very
complex densities. By using a sufﬁcient number of Gaussians, and by adjusting their
means and covariances as well as the coefﬁcients in the linear combination, almost
any continuous density can be approximated to arbitrary accuracy.
We therefore consider a superposition of K Gaussian densities of the form
p(x)=
K∑
k=1
πkN(x|µk,Σk) (2.188)
which is called a mixture of Gaussians . Each Gaussian density N(x|µk,Σk) is
called a component of the mixture and has its own mean µk and covariance Σk.
Contour and surface plots for a Gaussian mixture having 3 components are shown in
Figure 2.23.
In this section we shall consider Gaussian components to illustrate the frame-
work of mixture models. More generally, mixture models can comprise linear com-
binations of other distributions. For instance, in Section 9.3.3 we shall consider
mixtures of Bernoulli distributions as an example of a mixture model for discrete
variables.Section 9.3.3
The parameters π
k in (2.188) are called mixing coefﬁcients. If we integrate both
sides of (2.188) with respect tox, and note that bothp(x) and the individual Gaussian
components are normalized, we obtain
K∑
k=1
πk =1 . (2.189)
Also, the requirement that p(x) ⩾ 0, together with N(x|µk,Σk) ⩾ 0, implies
πk ⩾ 0 for all k. Combining this with the condition (2.189) we obtain
0 ⩽ πk ⩽ 1. (2.190)


## PDF Page 131

112 2. PROBABILITY DISTRIBUTIONS
0.5 0.3
0.2
(a)
0 0.5 1
0
0.5
1 (b)
0 0.5 1
0
0.5
1
Figure 2.23 Illustration of a mixture of 3 Gaussians in a two-dimensional space. (a) Contours of constant
density for each of the mixture components, in which the 3 components are denoted red, blue and green, and
the values of the mixing coefﬁcients are shown below each component. (b) Contours of the marginal probability
density p(x) of the mixture distribution. (c) A surface plot of the distribution p(x).
We therefore see that the mixing coefﬁcients satisfy the requirements to be probabil-
ities.
From the sum and product rules, the marginal density is given by
p(x)=
K∑
k=1
p(k)p(x|k) (2.191)
which is equivalent to (2.188) in which we can view πk = p(k) as the prior prob-
ability of picking the kth component, and the density N(x|µk,Σk)=p(x|k ) as
the probability of x conditioned on k. As we shall see in later chapters, an impor-
tant role is played by the posterior probabilities p(k|x), which are also known as
responsibilities. From Bayes’ theorem these are given by
γk(x) ≡ p(k|x)
= p(k)p(x|k)∑
l p(l)p(x|l)
= πkN(x|µk,Σk)∑
l πlN(x|µl,Σl). (2.192)
We shall discuss the probabilistic interpretation of the mixture distribution in greater
detail in Chapter 9.
The form of the Gaussian mixture distribution is governed by the parameters π,
µ and Σ, where we have used the notation π ≡{ π1,...,π K }, µ ≡{ µ1,..., µK }
and Σ ≡{ Σ1,... ΣK }. One way to set the values of these parameters is to use
maximum likelihood. From (2.188) the log of the likelihood function is given by
lnp(X|π, µ,Σ)=
N∑
n=1
ln
{ K∑
k=1
πkN(xn|µk,Σk)
}
(2.193)


## PDF Page 132

2.4. The Exponential Family 113
where X = {x1,..., xN }. We immediately see that the situation is now much
more complex than with a single Gaussian, due to the presence of the summation
over k inside the logarithm. As a result, the maximum likelihood solution for the
parameters no longer has a closed-form analytical solution. One approach to maxi-
mizing the likelihood function is to use iterative numerical optimization techniques
(Fletcher, 1987; Nocedal and Wright, 1999; Bishop and Nabney, 2008). Alterna-
tively we can employ a powerful framework calledexpectation maximization, which
will be discussed at length in Chapter 9.
2.4. The Exponential Family
The probability distributions that we have studied so far in this chapter (with the
exception of the Gaussian mixture) are speciﬁc examples of a broad class of distri-
butions called the exponential family (Duda and Hart, 1973; Bernardo and Smith,
1994). Members of the exponential family have many important properties in com-
mon, and it is illuminating to discuss these properties in some generality.
The exponential family of distributions overx, given parametersη, is deﬁned to
be the set of distributions of the form
p(x|η)=h(x)g (η)e x p
{
ηTu(x)
}
(2.194)
where x may be scalar or vector, and may be discrete or continuous. Here η are
called the natural parameters of the distribution, and u(x) is some function of x.
The function g(η) can be interpreted as the coefﬁcient that ensures that the distribu-
tion is normalized and therefore satisﬁes
g(η)
∫
h(x)e x p
{
ηTu(x)
}
dx =1 (2.195)
where the integration is replaced by summation if x is a discrete variable.
We begin by taking some examples of the distributions introduced earlier in
the chapter and showing that they are indeed members of the exponential family.
Consider ﬁrst the Bernoulli distribution
p(x|µ)=B e r n (x|µ)=µ x(1 − µ)1−x. (2.196)
Expressing the right-hand side as the exponential of the logarithm, we have
p(x|µ) = exp {xlnµ +( 1− x)l n ( 1− µ)}
=( 1 − µ)e x p
{
ln
( µ
1 − µ
)
x
}
. (2.197)
Comparison with (2.194) allows us to identify
η=l n
( µ
1 − µ
)
(2.198)


## PDF Page 133

114 2. PROBABILITY DISTRIBUTIONS
which we can solve for µ to give µ = σ(η), where
σ(η)= 1
1+e x p (−η) (2.199)
is called the logistic sigmoid function. Thus we can write the Bernoulli distribution
using the standard representation (2.194) in the form
p(x|η)= σ(−η) exp(ηx) (2.200)
where we have used 1 − σ(η)=σ (−η), which is easily proved from (2.199). Com-
parison with (2.194) shows that
u(x)= x (2.201)
h(x)=1 (2.202)
g(η)=σ (−η). (2.203)
Next consider the multinomial distribution that, for a single observationx, takes
the form
p(x|µ)=
M∏
k=1
µxk
k =e x p
{ M∑
k=1
xk ln µk
}
(2.204)
where x =( x1,...,x N )T. Again, we can write this in the standard representation
(2.194) so that
p(x|η)=e x p (ηTx) (2.205)
where ηk =l nµk, and we have deﬁned η =( η1,...,η M )T. Again, comparing with
(2.194) we have
u(x)=x (2.206)
h(x)=1 (2.207)
g(η)=1 . (2.208)
Note that the parameters ηk are not independent because the parameters µk are sub-
ject to the constraint
M∑
k=1
µk =1 (2.209)
so that, given anyM − 1 of the parameters µk, the value of the remaining parameter
is ﬁxed. In some circumstances, it will be convenient to remove this constraint by
expressing the distribution in terms of onlyM − 1 parameters. This can be achieved
by using the relationship (2.209) to eliminate µM by expressing it in terms of the
remaining {µk} where k =1 ,...,M − 1, thereby leaving M − 1 parameters. Note
that these remaining parameters are still subject to the constraints
0 ⩽ µk ⩽ 1,
M −1∑
k=1
µk ⩽ 1. (2.210)


## PDF Page 134

2.4. The Exponential Family 115
Making use of the constraint (2.209), the multinomial distribution in this representa-
tion then becomes
exp
{ M∑
k=1
xk ln µk
}
=e x p
{ M −1∑
k=1
xk lnµk +
(
1 −
M −1∑
k=1
xk
)
ln
(
1 −
M −1∑
k=1
µk
)}
=e x p
{ M −1∑
k=1
xk ln
(
µk
1 − ∑M −1
j=1 µj
)
+l n
(
1 −
M −1∑
k=1
µk
)}
. (2.211)
We now identify
ln
(
µk
1 − ∑
j µj
)
= ηk (2.212)
which we can solve for µk by ﬁrst summing both sides over k and then rearranging
and back-substituting to give
µk = exp(ηk)
1+ ∑
j exp(ηj). (2.213)
This is called the softmax function, or the normalized exponential. In this represen-
tation, the multinomial distribution therefore takes the form
p(x|η)=
(
1+
M −1∑
k=1
exp(ηk)
)−1
exp(ηTx). (2.214)
This is the standard form of the exponential family, with parameter vector η =
(η1,...,η M −1)T in which
u(x)=x (2.215)
h(x)=1 (2.216)
g(η)=
(
1+
M −1∑
k=1
exp(ηk)
)−1
. (2.217)
Finally, let us consider the Gaussian distribution. For the univariate Gaussian,
we have
p(x|µ, σ2)= 1
(2πσ2)1/2 exp
{
− 1
2σ2 (x − µ)2
}
(2.218)
= 1
(2πσ2)1/2 exp
{
− 1
2σ2 x2 + µ
σ2 x − 1
2σ2 µ2
}
(2.219)


## PDF Page 135

116 2. PROBABILITY DISTRIBUTIONS
which, after some simple rearrangement, can be cast in the standard exponential
family form (2.194) withExercise 2.57
η =
(
µ/σ2
−1/2σ2
)
(2.220)
u(x)=
(
x
x2
)
(2.221)
h(x)=( 2 π)−1/2 (2.222)
g(η)=( −2η2)1/2 exp
( η2
1
4η2
)
. (2.223)
2.4.1 Maximum likelihood and sufﬁcient statistics
Let us now consider the problem of estimating the parameter vectorη in the gen-
eral exponential family distribution (2.194) using the technique of maximum likeli-
hood. Taking the gradient of both sides of (2.195) with respect to η,w eh a v e
∇g(η)
∫
h(x)e x p
{
ηTu(x)
}
dx
+ g(η)
∫
h(x)e x p
{
ηTu(x)
}
u(x)dx =0 . (2.224)
Rearranging, and making use again of (2.195) then gives
− 1
g(η) ∇g(η)=g (η)
∫
h(x)e x p
{
ηTu(x)
}
u(x)dx = E[u(x)] (2.225)
where we have used (2.194). We therefore obtain the result
−∇ lng(η)=E[u(x )]. (2.226)
Note that the covariance ofu(x) can be expressed in terms of the second derivatives
of g(η), and similarly for higher order moments. Thus, provided we can normalize aExercise 2.58
distribution from the exponential family, we can always ﬁnd its moments by simple
differentiation.
Now consider a set of independent identically distributed data denoted by X =
{x1,..., xn}, for which the likelihood function is given by
p(X|η)=
( N∏
n=1
h(xn)
)
g(η)N exp
{
ηT
N∑
n=1
u(xn)
}
. (2.227)
Setting the gradient of ln p(X|η) with respect to η to zero, we get the following
condition to be satisﬁed by the maximum likelihood estimator ηML
−∇ lng(ηML)= 1
N
N∑
n=1
u(xn) (2.228)


## PDF Page 136

2.4. The Exponential Family 117
which can in principle be solved to obtain ηML. We see that the solution for the
maximum likelihood estimator depends on the data only through ∑
n u(xn), which
is therefore called the sufﬁcient statistic of the distribution (2.194). We do not need
to store the entire data set itself but only the value of the sufﬁcient statistic. For
the Bernoulli distribution, for example, the function u(x) is given just by x and
so we need only keep the sum of the data points {xn}, whereas for the Gaussian
u(x)=( x, x2)T, and so we should keep both the sum of{xn} and the sum of {x2
n}.
If we consider the limit N →∞ , then the right-hand side of (2.228) becomes
E[u(x)], and so by comparing with (2.226) we see that in this limit ηML will equal
the true value η.
In fact, this sufﬁciency property holds also for Bayesian inference, although
we shall defer discussion of this until Chapter 8 when we have equipped ourselves
with the tools of graphical models and can thereby gain a deeper insight into these
important concepts.
2.4.2 Conjugate priors
We have already encountered the concept of a conjugate prior several times, for
example in the context of the Bernoulli distribution (for which the conjugate prior
is the beta distribution) or the Gaussian (where the conjugate prior for the mean is
a Gaussian, and the conjugate prior for the precision is the Wishart distribution). In
general, for a given probability distribution p(x|η), we can seek a prior p(η) that is
conjugate to the likelihood function, so that the posterior distribution has the same
functional form as the prior. For any member of the exponential family (2.194), there
exists a conjugate prior that can be written in the form
p(η|χ,ν)=f (χ,ν)g(η)
ν exp
{
νηTχ
}
(2.229)
where f(χ,ν) is a normalization coefﬁcient, and g(η) is the same function as ap-
pears in (2.194). To see that this is indeed conjugate, let us multiply the prior (2.229)
by the likelihood function (2.227) to obtain the posterior distribution, up to a nor-
malization coefﬁcient, in the form
p(η|X, χ,ν) ∝ g(η)
ν+N exp
{
ηT
( N∑
n=1
u(xn)+ν χ
)}
. (2.230)
This again takes the same functional form as the prior (2.229), conﬁrming conjugacy.
Furthermore, we see that the parameter ν can be interpreted as a effective number of
pseudo-observations in the prior, each of which has a value for the sufﬁcient statistic
u(x) given by χ.
2.4.3 Noninformative priors
In some applications of probabilistic inference, we may have prior knowledge
that can be conveniently expressed through the prior distribution. For example, if
the prior assigns zero probability to some value of variable, then the posterior dis-
tribution will necessarily also assign zero probability to that value, irrespective of


## PDF Page 137

118 2. PROBABILITY DISTRIBUTIONS
any subsequent observations of data. In many cases, however, we may have little
idea of what form the distribution should take. We may then seek a form of prior
distribution, called a noninformative prior, which is intended to have as little inﬂu-
ence on the posterior distribution as possible (Jeffries, 1946; Box and Tao, 1973;
Bernardo and Smith, 1994). This is sometimes referred to as ‘letting the data speak
for themselves’.
If we have a distributionp(x|λ)governed by a parameterλ, we might be tempted
to propose a prior distribution p(λ) = const as a suitable prior. If λ is a discrete
variable with K states, this simply amounts to setting the prior probability of each
state to 1/K. In the case of continuous parameters, however, there are two potential
difﬁculties with this approach. The ﬁrst is that, if the domain of λ is unbounded,
this prior distribution cannot be correctly normalized because the integral over λ
diverges. Such priors are called improper. In practice, improper priors can often
be used provided the corresponding posterior distribution is proper, i.e., that it can
be correctly normalized. For instance, if we put a uniform prior distribution over
the mean of a Gaussian, then the posterior distribution for the mean, once we have
observed at least one data point, will be proper.
A second difﬁculty arises from the transformation behaviour of a probability
density under a nonlinear change of variables, given by (1.27). If a function h(λ)
is constant, and we change variables to λ = η
2, then ˆh(η)= h(η2) will also be
constant. However, if we choose the density pλ(λ) to be constant, then the density
of ηwill be given, from (1.27), by
pη(η)= pλ(λ)
⏐⏐⏐⏐
dλ
dη
⏐
⏐⏐⏐
= pλ(η2)2η ∝ η (2.231)
and so the density overηwill not be constant. This issue does not arise when we use
maximum likelihood, because the likelihood function p(x|λ) is a simple function of
λ and so we are free to use any convenient parameterization. If, however, we are to
choose a prior distribution that is constant, we must take care to use an appropriate
representation for the parameters.
Here we consider two simple examples of noninformative priors (Berger, 1985).
First of all, if a density takes the form
p(x|µ)=f (x − µ) (2.232)
then the parameter µ is known as a location parameter . This family of densities
exhibits translation invariance because if we shift x by a constant to give ˆx = x+c,
then
p(ˆx|ˆµ)=f (ˆx − ˆµ) (2.233)
where we have deﬁned ˆµ = µ + c. Thus the density takes the same form in the
new variable as in the original one, and so the density is independent of the choice
of origin. We would like to choose a prior distribution that reﬂects this translation
invariance property, and so we choose a prior that assigns equal probability mass to


## PDF Page 138

2.4. The Exponential Family 119
an interval A ⩽ µ ⩽ B as to the shifted interval A − c ⩽ µ ⩽ B − c. This implies
∫ B
A
p(µ)d µ =
∫ B−c
A−c
p(µ)d µ =
∫ B
A
p(µ − c)dµ (2.234)
and because this must hold for all choices of A and B,w eh a v e
p(µ − c)=p(µ ) (2.235)
which implies that p(µ) is constant. An example of a location parameter would be
the mean µ of a Gaussian distribution. As we have seen, the conjugate prior distri-
bution for µ in this case is a Gaussian p(µ|µ0,σ2
0)= N(µ|µ0,σ2
0), and we obtain a
noninformative prior by taking the limit σ2
0 →∞ . Indeed, from (2.141) and (2.142)
we see that this gives a posterior distribution overµ in which the contributions from
the prior vanish.
As a second example, consider a density of the form
p(x|σ)= 1
σf
(x
σ
)
(2.236)
where σ> 0. Note that this will be a normalized density provided f(x) is correctly
normalized. The parameter σ is known as ascale parameter, and the density exhibitsExercise 2.59
scale invariance because if we scale x by a constant to give ˆx = cx, then
p(ˆx|ˆσ)= 1
ˆσf
(ˆx
ˆσ
)
(2.237)
where we have deﬁned ˆσ = cσ. This transformation corresponds to a change of
scale, for example from meters to kilometers if x is a length, and we would like
to choose a prior distribution that reﬂects this scale invariance. If we consider an
interval A ⩽ σ ⩽ B, and a scaled interval A/c ⩽ σ ⩽ B/c, then the prior should
assign equal probability mass to these two intervals. Thus we have
∫ B
A
p(σ)d σ =
∫ B/c
A/c
p(σ)d σ =
∫ B
A
p
(1
cσ
) 1
c dσ (2.238)
and because this must hold for choices of A and B,w eh a v e
p(σ)=p
(1
cσ
) 1
c (2.239)
and hence p(σ) ∝ 1/σ. Note that again this is an improper prior because the integral
of the distribution over 0 ⩽ σ ⩽ ∞ is divergent. It is sometimes also convenient
to think of the prior distribution for a scale parameter in terms of the density of the
log of the parameter. Using the transformation rule (1.27) for densities we see that
p(lnσ) = const. Thus, for this prior there is the same probability mass in the range
1 ⩽ σ ⩽ 10 as in the range 10 ⩽ σ ⩽ 100 and in 100 ⩽ σ ⩽ 1000.


## PDF Page 139

120 2. PROBABILITY DISTRIBUTIONS
An example of a scale parameter would be the standard deviationσ of a Gaussian
distribution, after we have taken account of the location parameter µ, because
N(x|µ, σ2) ∝ σ−1 exp
{
−(˜x/σ)2}
(2.240)
where ˜x = x − µ. As discussed earlier, it is often more convenient to work in terms
of the precision λ =1 /σ2 rather than σ itself. Using the transformation rule for
densities, we see that a distribution p(σ) ∝ 1/σ corresponds to a distribution over λ
of the form p(λ) ∝ 1/λ. We have seen that the conjugate prior forλ was the gamma
distribution Gam(λ|a0,b0) given by (2.146). The noninformative prior is obtainedSection 2.3
as the special casea0 = b0 =0 . Again, if we examine the results (2.150) and (2.151)
for the posterior distribution ofλ, we see that fora0 = b0 =0 , the posterior depends
only on terms arising from the data and not from the prior.
2.5. Nonparametric Methods
Throughout this chapter, we have focussed on the use of probability distributions
having speciﬁc functional forms governed by a small number of parameters whose
values are to be determined from a data set. This is called the parametric approach
to density modelling. An important limitation of this approach is that the chosen
density might be a poor model of the distribution that generates the data, which can
result in poor predictive performance. For instance, if the process that generates the
data is multimodal, then this aspect of the distribution can never be captured by a
Gaussian, which is necessarily unimodal.
In this ﬁnal section, we consider some nonparametric approaches to density es-
timation that make few assumptions about the form of the distribution. Here we shall
focus mainly on simple frequentist methods. The reader should be aware, however,
that nonparametric Bayesian methods are attracting increasing interest (Walkeret al.,
1999; Neal, 2000; M¨uller and Quintana, 2004; Teh et al., 2006).
Let us start with a discussion of histogram methods for density estimation, which
we have already encountered in the context of marginal and conditional distributions
in Figure 1.11 and in the context of the central limit theorem in Figure 2.6. Here we
explore the properties of histogram density models in more detail, focussing on the
case of a single continuous variable x. Standard histograms simply partition x into
distinct bins of width ∆
i and then count the number ni of observations of x falling
in bin i. In order to turn this count into a normalized probability density, we simply
divide by the total number N of observations and by the width ∆ i of the bins to
obtain probability values for each bin given by
pi = ni
N∆ i
(2.241)
for which it is easily seen that
∫
p(x)d x =1 . This gives a model for the density
p(x) that is constant over the width of each bin, and often the bins are chosen to have
the same width ∆ i =∆ .


## PDF Page 140

2.5. Nonparametric Methods 121
Figure 2.24 An illustration of the histogram approach
to density estimation, in which a data set
of 50 data points is generated from the
distribution shown by the green curve.
Histogram density estimates, based on
(2.241), with a common bin width ∆ are
shown for various values of ∆.
∆=0 .04
0 0.5 1
0
5
∆=0 .08
0 0.5 1
0
5
∆=0 .25
0 0.5 1
0
5
In Figure 2.24, we show an example of histogram density estimation. Here
the data is drawn from the distribution, corresponding to the green curve, which is
formed from a mixture of two Gaussians. Also shown are three examples of his-
togram density estimates corresponding to three different choices for the bin width
∆ . We see that when∆ is very small (top ﬁgure), the resulting density model is very
spiky, with a lot of structure that is not present in the underlying distribution that
generated the data set. Conversely, if∆ is too large (bottom ﬁgure) then the result is
a model that is too smooth and that consequently fails to capture the bimodal prop-
erty of the green curve. The best results are obtained for some intermediate value
of ∆ (middle ﬁgure). In principle, a histogram density model is also dependent on
the choice of edge location for the bins, though this is typically much less signiﬁcant
than the value of ∆ .
Note that the histogram method has the property (unlike the methods to be dis-
cussed shortly) that, once the histogram has been computed, the data set itself can
be discarded, which can be advantageous if the data set is large. Also, the histogram
approach is easily applied if the data points are arriving sequentially.
In practice, the histogram technique can be useful for obtaining a quick visual-
ization of data in one or two dimensions but is unsuited to most density estimation
applications. One obvious problem is that the estimated density has discontinuities
that are due to the bin edges rather than any property of the underlying distribution
that generated the data. Another major limitation of the histogram approach is its
scaling with dimensionality. If we divide each variable in a D-dimensional space
into M bins, then the total number of bins will be M
D. This exponential scaling
with D is an example of the curse of dimensionality. In a space of high dimensional-Section 1.4
ity, the quantity of data needed to provide meaningful estimates of local probability
density would be prohibitive.
The histogram approach to density estimation does, however, teach us two im-
portant lessons. First, to estimate the probability density at a particular location,
we should consider the data points that lie within some local neighbourhood of that
point. Note that the concept of locality requires that we assume some form of dis-
tance measure, and here we have been assuming Euclidean distance. For histograms,


## PDF Page 141

122 2. PROBABILITY DISTRIBUTIONS
this neighbourhood property was deﬁned by the bins, and there is a natural ‘smooth-
ing’ parameter describing the spatial extent of the local region, in this case the bin
width. Second, the value of the smoothing parameter should be neither too large nor
too small in order to obtain good results. This is reminiscent of the choice of model
complexity in polynomial curve ﬁtting discussed in Chapter 1 where the degree M
of the polynomial, or alternatively the value α of the regularization parameter, was
optimal for some intermediate value, neither too large nor too small. Armed with
these insights, we turn now to a discussion of two widely used nonparametric tech-
niques for density estimation, kernel estimators and nearest neighbours, which have
better scaling with dimensionality than the simple histogram model.
2.5.1 Kernel density estimators
Let us suppose that observations are being drawn from some unknown probabil-
ity density p(x) in some D-dimensional space, which we shall take to be Euclidean,
and we wish to estimate the value of p(x). From our earlier discussion of locality,
let us consider some small region R containing x. The probability mass associated
with this region is given by
P =
∫
R
p(x)dx. (2.242)
Now suppose that we have collected a data set comprising N observations drawn
from p(x). Because each data point has a probability P of falling within R, the total
number K of points that lie inside R will be distributed according to the binomial
distributionSection 2.1
Bin(K|N,P )= N!
K!(N − K)!PK(1 − P)1−K. (2.243)
Using (2.11), we see that the mean fraction of points falling inside the region is
E[K/N]= P , and similarly using (2.12) we see that the variance around this mean
is var[K/N]=P (1 − P)/N. For large N, this distribution will be sharply peaked
around the mean and so
K ≃ NP. (2.244)
If, however, we also assume that the regionR is sufﬁciently small that the probability
density p(x) is roughly constant over the region, then we have
P ≃ p(x)V (2.245)
where V is the volume of R. Combining (2.244) and (2.245), we obtain our density
estimate in the form
p(x)= K
NV . (2.246)
Note that the validity of (2.246) depends on two contradictory assumptions, namely
that the region R be sufﬁciently small that the density is approximately constant over
the region and yet sufﬁciently large (in relation to the value of that density) that the
number K of points falling inside the region is sufﬁcient for the binomial distribution
to be sharply peaked.


## PDF Page 142

2.5. Nonparametric Methods 123
We can exploit the result (2.246) in two different ways. Either we can ﬁx K and
determine the value ofV from the data, which gives rise to theK-nearest-neighbour
technique discussed shortly, or we can ﬁx V and determine K from the data, giv-
ing rise to the kernel approach. It can be shown that both the K-nearest-neighbour
density estimator and the kernel density estimator converge to the true probability
density in the limit N →∞ provided V shrinks suitably with N, and K grows with
N (Duda and Hart, 1973).
We begin by discussing the kernel method in detail, and to start with we take
the region R to be a small hypercube centred on the point x at which we wish to
determine the probability density. In order to count the number K of points falling
within this region, it is convenient to deﬁne the following function
k(u)=
{
1, |ui| ⩽ 1/2, i =1 ,...,D ,
0, otherwise (2.247)
which represents a unit cube centred on the origin. The function k(u) is an example
of a kernel function, and in this context is also called aParzen window. From (2.247),
the quantity k((x − xn)/h) will be one if the data pointxn lies inside a cube of side
h centred on x, and zero otherwise. The total number of data points lying inside this
cube will therefore be
K =
N∑
n=1
k
(x − xn
h
)
. (2.248)
Substituting this expression into (2.246) then gives the following result for the esti-
mated density at x
p(x)= 1
N
N∑
n=1
1
hD k
(x − xn
h
)
(2.249)
where we have used V = hD for the volume of a hypercube of side h in D di-
mensions. Using the symmetry of the function k(u), we can now re-interpret this
equation, not as a single cube centred on x but as the sum over N cubes centred on
the N data points xn.
As it stands, the kernel density estimator (2.249) will suffer from one of the same
problems that the histogram method suffered from, namely the presence of artiﬁcial
discontinuities, in this case at the boundaries of the cubes. We can obtain a smoother
density model if we choose a smoother kernel function, and a common choice is the
Gaussian, which gives rise to the following kernel density model
p(x)= 1
N
N∑
n=1
1
(2πh2)1/2 exp
{
− ∥x − xn∥2
2h2
}
(2.250)
where h represents the standard deviation of the Gaussian components. Thus our
density model is obtained by placing a Gaussian over each data point and then adding
up the contributions over the whole data set, and then dividing byN so that the den-
sity is correctly normalized. In Figure 2.25, we apply the model (2.250) to the data


## PDF Page 143

124 2. PROBABILITY DISTRIBUTIONS
Figure 2.25 Illustration of the kernel density model
(2.250) applied to the same data set used
to demonstrate the histogram approach in
Figure 2.24. We see that h acts as a
smoothing parameter and that if it is set
too small (top panel), the result is a very
noisy density model, whereas if it is set
too large (bottom panel), then the bimodal
nature of the underlying distribution from
which the data is generated (shown by the
green curve) is washed out. The best den-
sity model is obtained for some intermedi-
ate value of h (middle panel).
h =0 .005
0 0.5 1
0
5
h =0 .07
0 0.5 1
0
5
h =0 .2
0 0.5 1
0
5
set used earlier to demonstrate the histogram technique. We see that, as expected,
the parameter h plays the role of a smoothing parameter, and there is a trade-off
between sensitivity to noise at small h and over-smoothing at large h. Again, the
optimization of h is a problem in model complexity, analogous to the choice of bin
width in histogram density estimation, or the degree of the polynomial used in curve
ﬁtting.
We can choose any other kernel function k(u) in (2.249) subject to the condi-
tions
k(u) ⩾ 0, (2.251)
∫
k(u)du =1 (2.252)
which ensure that the resulting probability distribution is nonnegative everywhere
and integrates to one. The class of density model given by (2.249) is called a kernel
density estimator, or Parzen estimator. It has a great merit that there is no compu-
tation involved in the ‘training’ phase because this simply requires storage of the
training set. However, this is also one of its great weaknesses because the computa-
tional cost of evaluating the density grows linearly with the size of the data set.
2.5.2 Nearest-neighbour methods
One of the difﬁculties with the kernel approach to density estimation is that the
parameter h governing the kernel width is ﬁxed for all kernels. In regions of high
data density, a large value of h may lead to over-smoothing and a washing out of
structure that might otherwise be extracted from the data. However, reducing h may
lead to noisy estimates elsewhere in data space where the density is smaller. Thus
the optimal choice for h may be dependent on location within the data space. This
issue is addressed by nearest-neighbour methods for density estimation.
We therefore return to our general result (2.246) for local density estimation,
and instead of ﬁxing V and determining the value of K from the data, we consider
a ﬁxed value of K and use the data to ﬁnd an appropriate value for V . To do this,
we consider a small sphere centred on the point x at which we wish to estimate the


## PDF Page 144

2.5. Nonparametric Methods 125
Figure 2.26 Illustration of K-nearest-neighbour den-
sity estimation using the same data set
as in Figures 2.25 and 2.24. We see
that the parameter K governs the degree
of smoothing, so that a small value of
K leads to a very noisy density model
(top panel), whereas a large value (bot-
tom panel) smoothes out the bimodal na-
ture of the true distribution (shown by the
green curve) from which the data set was
generated.
K =1
0 0.5 1
0
5
K =5
0 0.5 1
0
5
K =3 0
0 0.5 1
0
5
density p(x), and we allow the radius of the sphere to grow until it contains precisely
K data points. The estimate of the densityp(x) is then given by (2.246) withV set to
the volume of the resulting sphere. This technique is known asK nearest neighbours
and is illustrated in Figure 2.26, for various choices of the parameter K, using the
same data set as used in Figure 2.24 and Figure 2.25. We see that the value of K
now governs the degree of smoothing and that again there is an optimum choice for
K that is neither too large nor too small. Note that the model produced byK nearest
neighbours is not a true density model because the integral over all space diverges.Exercise 2.61
We close this chapter by showing how the K-nearest-neighbour technique for
density estimation can be extended to the problem of classiﬁcation. To do this, we
apply the K-nearest-neighbour density estimation technique to each class separately
and then make use of Bayes’ theorem. Let us suppose that we have a data set com-
prising Nk points in class Ck with N points in total, so that ∑
k Nk = N.I f w e
wish to classify a new point x, we draw a sphere centred on x containing precisely
K points irrespective of their class. Suppose this sphere has volume V and contains
Kk points from class Ck. Then (2.246) provides an estimate of the density associated
with each class
p(x|Ck)= Kk
NkV . (2.253)
Similarly, the unconditional density is given by
p(x)= K
NV (2.254)
while the class priors are given by
p(Ck)= Nk
N . (2.255)
We can now combine (2.253), (2.254), and (2.255) using Bayes’ theorem to obtain
the posterior probability of class membership
p(C
k|x)= p(x|Ck)p(Ck)
p(x) = Kk
K . (2.256)


## PDF Page 145

126 2. PROBABILITY DISTRIBUTIONS
Figure 2.27 (a) In the K-nearest-
neighbour classiﬁer, a new point,
shown by the black diamond, is clas-
siﬁed according to the majority class
membership of the K closest train-
ing data points, in this case K =
3. (b) In the nearest-neighbour
(K =1 ) approach to classiﬁcation,
the resulting decision boundary is
composed of hyperplanes that form
perpendicular bisectors of pairs of
points from different classes.
x1
x2
(a)
x1
x2
(b)
If we wish to minimize the probability of misclassiﬁcation, this is done by assigning
the test point x to the class having the largest posterior probability, corresponding to
the largest value of Kk/K. Thus to classify a new point, we identify the K nearest
points from the training data set and then assign the new point to the class having the
largest number of representatives amongst this set. Ties can be broken at random.
The particular case of K =1 is called the nearest-neighbour rule, because a test
point is simply assigned to the same class as the nearest point from the training set.
These concepts are illustrated in Figure 2.27.
In Figure 2.28, we show the results of applying the K-nearest-neighbour algo-
rithm to the oil ﬂow data, introduced in Chapter 1, for various values of K.A s
expected, we see that K controls the degree of smoothing, so that small K produces
many small regions of each class, whereas large K leads to fewer larger regions.
x6
x7
K =1
0 1 2
0
1
2
x6
x7
K =3
0 1 2
0
1
2
x6
x7
K =31
0 1 2
0
1
2
Figure 2.28 Plot of 200 data points from the oil data set showing values of x6 plotted against x7, where the
red, green, and blue points correspond to the ‘laminar’, ‘annular’, and ‘homogeneous’ classes, respectively. Also
shown are the classiﬁcations of the input space given by the K-nearest-neighbour algorithm for various values
of K.


## PDF Page 146

Exercises 127
An interesting property of the nearest-neighbour (K =1 ) classiﬁer is that, in the
limit N →∞ , the error rate is never more than twice the minimum achievable error
rate of an optimal classiﬁer, i.e., one that uses the true class distributions (Cover and
Hart, 1967) .
As discussed so far, both the K-nearest-neighbour method, and the kernel den-
sity estimator, require the entire training data set to be stored, leading to expensive
computation if the data set is large. This effect can be offset, at the expense of some
additional one-off computation, by constructing tree-based search structures to allow
(approximate) near neighbours to be found efﬁciently without doing an exhaustive
search of the data set. Nevertheless, these nonparametric methods are still severely
limited. On the other hand, we have seen that simple parametric models are very
restricted in terms of the forms of distribution that they can represent. We therefore
need to ﬁnd density models that are very ﬂexible and yet for which the complexity
of the models can be controlled independently of the size of the training set, and we
shall see in subsequent chapters how to achieve this.
Exercises
2.1 (⋆) www Verify that the Bernoulli distribution (2.2) satisﬁes the following prop-
erties
1∑
x=0
p(x|µ)=1 (2.257)
E[x]= µ (2.258)
var[x]= µ(1 − µ). (2.259)
Show that the entropy H[x] of a Bernoulli distributed random binary variable x is
given by
H[x]=−µ ln µ − (1 − µ)l n ( 1− µ). (2.260)
2.2 (⋆⋆ ) The form of the Bernoulli distribution given by (2.2) is not symmetric be-
tween the two values of x. In some situations, it will be more convenient to use an
equivalent formulation for which x ∈{ −1, 1}, in which case the distribution can be
written
p(x|µ)=
(1 − µ
2
)(1−x)/2 (1+ µ
2
)(1+x)/2
(2.261)
where µ ∈ [−1, 1]. Show that the distribution (2.261) is normalized, and evaluate its
mean, variance, and entropy.
2.3 (⋆⋆ ) www In this exercise, we prove that the binomial distribution (2.9) is nor-
malized. First use the deﬁnition (2.10) of the number of combinations of m identical
objects chosen from a total of N to show that
(N
m
)
+
( N
m − 1
)
=
(N +1
m
)
. (2.262)


## PDF Page 147

128 2. PROBABILITY DISTRIBUTIONS
Use this result to prove by induction the following result
(1 +x)N =
N∑
m=0
(N
m
)
xm (2.263)
which is known as the binomial theorem, and which is valid for all real values of x.
Finally, show that the binomial distribution is normalized, so that
N∑
m=0
(N
m
)
µm(1 − µ)N −m =1 (2.264)
which can be done by ﬁrst pulling out a factor (1 − µ)N out of the summation and
then making use of the binomial theorem.
2.4 (⋆⋆ ) Show that the mean of the binomial distribution is given by (2.11). To do this,
differentiate both sides of the normalization condition (2.264) with respect to µ and
then rearrange to obtain an expression for the mean ofn. Similarly, by differentiating
(2.264) twice with respect to µ and making use of the result (2.11) for the mean of
the binomial distribution prove the result (2.12) for the variance of the binomial.
2.5 (⋆⋆ ) www In this exercise, we prove that the beta distribution, given by (2.13), is
correctly normalized, so that (2.14) holds. This is equivalent to showing that
∫ 1
0
µa−1(1 − µ)b−1 dµ = Γ(a)Γ(b)
Γ(a + b) . (2.265)
From the deﬁnition (1.141) of the gamma function, we have
Γ(a)Γ(b)=
∫ ∞
0
exp(−x)xa−1 dx
∫ ∞
0
exp(−y)yb−1 dy. (2.266)
Use this expression to prove (2.265) as follows. First bring the integral overy inside
the integrand of the integral over x, next make the change of variable t = y + x
where x is ﬁxed, then interchange the order of the x and t integrations, and ﬁnally
make the change of variable x = tµ where t is ﬁxed.
2.6 (⋆) Make use of the result (2.265) to show that the mean, variance, and mode of the
beta distribution (2.13) are given respectively by
E[µ]= a
a + b (2.267)
var[µ]= ab
(a + b)2(a + b +1 ) (2.268)
mode[µ]= a − 1
a + b − 2. (2.269)


## PDF Page 148

Exercises 129
2.7 (⋆⋆ ) Consider a binomial random variable x given by (2.9), with prior distribution
for µ given by the beta distribution (2.13), and suppose we have observed m occur-
rences of x =1 and l occurrences of x =0 . Show that the posterior mean value ofx
lies between the prior mean and the maximum likelihood estimate for µ. To do this,
show that the posterior mean can be written as λ times the prior mean plus (1 − λ)
times the maximum likelihood estimate, where 0 ⩽ λ ⩽ 1. This illustrates the con-
cept of the posterior distribution being a compromise between the prior distribution
and the maximum likelihood solution.
2.8 (⋆) Consider two variablesx and y with joint distributionp(x, y). Prove the follow-
ing two results
E[x]= Ey [Ex[x|y]] (2.270)
var[x]= Ey [varx[x|y]] + vary [Ex[x|y]]. (2.271)
Here Ex[x|y] denotes the expectation of x under the conditional distribution p(x|y),
with a similar notation for the conditional variance.
2.9 (⋆⋆⋆ ) www . In this exercise, we prove the normalization of the Dirichlet dis-
tribution (2.38) using induction. We have already shown in Exercise 2.5 that the
beta distribution, which is a special case of the Dirichlet for M =2 , is normalized.
We now assume that the Dirichlet distribution is normalized for M − 1 variables
and prove that it is normalized for M variables. To do this, consider the Dirichlet
distribution over M variables, and take account of the constraint ∑M
k=1 µk =1 by
eliminating µM , so that the Dirichlet is written
pM (µ1,...,µ M −1)=C M
M −1∏
k=1
µαk −1
k
(
1 −
M −1∑
j=1
µj
)αM −1
(2.272)
and our goal is to ﬁnd an expression for CM . To do this, integrate overµM −1, taking
care over the limits of integration, and then make a change of variable so that this
integral has limits 0 and 1. By assuming the correct result for CM −1 and making use
of (2.265), derive the expression for CM .
2.10 (⋆⋆ ) Using the property Γ(x +1 ) = xΓ(x) of the gamma function, derive the
following results for the mean, variance, and covariance of the Dirichlet distribution
given by (2.38)
E[µ
j]= αj
α0
(2.273)
var[µj]= αj(α0 − αj)
α2
0(α0 +1 ) (2.274)
cov[µjµl]= − αjαl
α2
0(α0 +1 ),j ̸= l (2.275)
where α0 is deﬁned by (2.39).


## PDF Page 149

130 2. PROBABILITY DISTRIBUTIONS
2.11 (⋆) www By expressing the expectation of lnµj under the Dirichlet distribution
(2.38) as a derivative with respect toαj , show that
E[lnµj]= ψ(αj) − ψ(α0) (2.276)
where α0 is given by (2.39) and
ψ(a) ≡ d
da ln Γ(a) (2.277)
is the digamma function.
2.12 (⋆) The uniform distribution for a continuous variable x is deﬁned by
U(x|a, b)= 1
b − a,a ⩽ x ⩽ b. (2.278)
Verify that this distribution is normalized, and ﬁnd expressions for its mean and
variance.
2.13 (⋆⋆ ) Evaluate the Kullback-Leibler divergence (1.113) between two Gaussians
p(x)=N (x|µ,Σ) and q(x)=N (x|m,L).
2.14 (⋆⋆ ) www This exercise demonstrates that the multivariate distribution with max-
imum entropy, for a given covariance, is a Gaussian. The entropy of a distribution
p(x) is given by
H[x]=−
∫
p(x)l np(x)dx. (2.279)
We wish to maximize H[x] over all distributions p(x) subject to the constraints that
p(x) be normalized and that it have a speciﬁc mean and covariance, so that
∫
p(x)dx =1 (2.280)
∫
p(x)xdx = µ (2.281)
∫
p(x)(x − µ)(x − µ)T dx = Σ. (2.282)
By performing a variational maximization of (2.279) and using Lagrange multipliers
to enforce the constraints (2.280), (2.281), and (2.282), show that the maximum
likelihood distribution is given by the Gaussian (2.43).
2.15 (⋆⋆ ) Show that the entropy of the multivariate Gaussian N(x|µ,Σ) is given by
H[x]= 1
2 ln |Σ| + D
2 (1 + ln(2π)) (2.283)
where D is the dimensionality of x.


## PDF Page 150

Exercises 131
2.16 (⋆⋆⋆ ) www Consider two random variables x1 and x2 having Gaussian distri-
butions with means µ1,µ2 and precisions τ1, τ2 respectively. Derive an expression
for the differential entropy of the variable x = x1 + x2. To do this, ﬁrst ﬁnd the
distribution of x by using the relation
p(x)=
∫ ∞
−∞
p(x|x2)p(x2)d x2 (2.284)
and completing the square in the exponent. Then observe that this represents the
convolution of two Gaussian distributions, which itself will be Gaussian, and ﬁnally
make use of the result (1.110) for the entropy of the univariate Gaussian.
2.17 (⋆) www Consider the multivariate Gaussian distribution given by (2.43). By
writing the precision matrix (inverse covariance matrix) Σ−1 as the sum of a sym-
metric and an anti-symmetric matrix, show that the anti-symmetric term does not
appear in the exponent of the Gaussian, and hence that the precision matrix may be
taken to be symmetric without loss of generality. Because the inverse of a symmetric
matrix is also symmetric (see Exercise 2.22), it follows that the covariance matrix
may also be chosen to be symmetric without loss of generality.
2.18 (⋆⋆⋆ ) Consider a real, symmetric matrix Σ whose eigenvalue equation is given
by (2.45). By taking the complex conjugate of this equation and subtracting the
original equation, and then forming the inner product with eigenvectoru
i, show that
the eigenvalues λi are real. Similarly, use the symmetry property of Σ to show that
two eigenvectorsui and uj will be orthogonal provided λj ̸= λi. Finally, show that
without loss of generality, the set of eigenvectors can be chosen to be orthonormal,
so that they satisfy (2.46), even if some of the eigenvalues are zero.
2.19 (⋆⋆ ) Show that a real, symmetric matrix Σ having the eigenvector equation (2.45)
can be expressed as an expansion in the eigenvectors, with coefﬁcients given by the
eigenvalues, of the form (2.48). Similarly, show that the inverse matrix Σ
−1 has a
representation of the form (2.49).
2.20 (⋆⋆ ) www A positive deﬁnite matrix Σ can be deﬁned as one for which the
quadratic form
aTΣa (2.285)
is positive for any real value of the vector a. Show that a necessary and sufﬁcient
condition for Σ to be positive deﬁnite is that all of the eigenvalues λi of Σ, deﬁned
by (2.45), are positive.
2.21 (⋆) Show that a real, symmetric matrix of sizeD ×D has D(D+1)/2 independent
parameters.
2.22 (⋆) www Show that the inverse of a symmetric matrix is itself symmetric.
2.23 (⋆⋆ ) By diagonalizing the coordinate system using the eigenvector expansion (2.45),
show that the volume contained within the hyperellipsoid corresponding to a constant


## PDF Page 151

132 2. PROBABILITY DISTRIBUTIONS
Mahalanobis distance ∆ is given by
VD|Σ|1/2∆ D (2.286)
where VD is the volume of the unit sphere in D dimensions, and the Mahalanobis
distance is deﬁned by (2.44).
2.24 (⋆⋆ ) www Prove the identity (2.76) by multiplying both sides by the matrix
(
AB
CD
)
(2.287)
and making use of the deﬁnition (2.77).
2.25 (⋆⋆ ) In Sections 2.3.1 and 2.3.2, we considered the conditional and marginal distri-
butions for a multivariate Gaussian. More generally, we can consider a partitioning
of the components of x into three groups xa, xb, and xc, with a corresponding par-
titioning of the mean vector µ and of the covariance matrix Σ in the form
µ =
(µa
µb
µc
)
, Σ =
(Σaa Σab Σac
Σba Σbb Σbc
Σca Σcb Σcc
)
. (2.288)
By making use of the results of Section 2.3, ﬁnd an expression for the conditional
distribution p(xa|xb) in which xc has been marginalized out.
2.26 (⋆⋆ ) A very useful result from linear algebra is the Woodbury matrix inversion
formula given by
(A + BCD)−1 = A−1 − A−1B(C−1 + DA−1B)−1DA−1. (2.289)
By multiplying both sides by (A + BCD) prove the correctness of this result.
2.27 (⋆) Let x and z be two independent random vectors, so that p(x,z)= p(x)p(z).
Show that the mean of their sumy = x+z is given by the sum of the means of each
of the variable separately. Similarly, show that the covariance matrix ofy is given by
the sum of the covariance matrices of x and z. Conﬁrm that this result agrees with
that of Exercise 1.10.
2.28 (⋆⋆⋆ ) www Consider a joint distribution over the variable
z =
(
x
y
)
(2.290)
whose mean and covariance are given by (2.108) and (2.105) respectively. By mak-
ing use of the results (2.92) and (2.93) show that the marginal distribution p(x) is
given (2.99). Similarly, by making use of the results (2.81) and (2.82) show that the
conditional distribution p(y|x) is given by (2.100).


## PDF Page 152

Exercises 133
2.29 (⋆⋆ ) Using the partitioned matrix inversion formula (2.76), show that the inverse of
the precision matrix (2.104) is given by the covariance matrix (2.105).
2.30 (⋆) By starting from (2.107) and making use of the result (2.105), verify the result
(2.108).
2.31 (⋆⋆ ) Consider two multidimensional random vectors x and z having Gaussian
distributions p(x)= N(x|µx,Σx) and p(z)=N (z|µz,Σz) respectively, together
with their sumy = x+z. Use the results (2.109) and (2.110) to ﬁnd an expression for
the marginal distribution p(y) by considering the linear-Gaussian model comprising
the product of the marginal distributionp(x) and the conditional distributionp(y|x).
2.32 (⋆⋆⋆ ) www This exercise and the next provide practice at manipulating the
quadratic forms that arise in linear-Gaussian models, as well as giving an indepen-
dent check of results derived in the main text. Consider a joint distribution p(x,y)
deﬁned by the marginal and conditional distributions given by (2.99) and (2.100).
By examining the quadratic form in the exponent of the joint distribution, and using
the technique of ‘completing the square’ discussed in Section 2.3, ﬁnd expressions
for the mean and covariance of the marginal distribution p(y) in which the variable
x has been integrated out. To do this, make use of the Woodbury matrix inversion
formula (2.289). Verify that these results agree with (2.109) and (2.110) obtained
using the results of Chapter 2.
2.33 (⋆⋆⋆ ) Consider the same joint distribution as in Exercise 2.32, but now use the
technique of completing the square to ﬁnd expressions for the mean and covariance
of the conditional distribution p(x|y). Again, verify that these agree with the corre-
sponding expressions (2.111) and (2.112).
2.34 (⋆⋆ )
www To ﬁnd the maximum likelihood solution for the covariance matrix
of a multivariate Gaussian, we need to maximize the log likelihood function (2.118)
with respect to Σ, noting that the covariance matrix must be symmetric and positive
deﬁnite. Here we proceed by ignoring these constraints and doing a straightforward
maximization. Using the results (C.21), (C.26), and (C.28) from Appendix C, show
that the covariance matrix Σ that maximizes the log likelihood function (2.118) is
given by the sample covariance (2.122). We note that the ﬁnal result is necessarily
symmetric and positive deﬁnite (provided the sample covariance is nonsingular).
2.35 (⋆⋆ ) Use the result (2.59) to prove (2.62). Now, using the results (2.59), and (2.62),
show that
E[x
nxm]=µµ T + InmΣ (2.291)
where xn denotes a data point sampled from a Gaussian distribution with mean µ
and covarianceΣ, and Inm denotes the (n, m)element of the identity matrix. Hence
prove the result (2.124).
2.36 (⋆⋆ ) www Using an analogous procedure to that used to obtain (2.126), derive
an expression for the sequential estimation of the variance of a univariate Gaussian


## PDF Page 153

134 2. PROBABILITY DISTRIBUTIONS
distribution, by starting with the maximum likelihood expression
σ2
ML = 1
N
N∑
n=1
(xn − µ)2. (2.292)
Verify that substituting the expression for a Gaussian distribution into the Robbins-
Monro sequential estimation formula (2.135) gives a result of the same form, and
hence obtain an expression for the corresponding coefﬁcients a
N .
2.37 (⋆⋆ ) Using an analogous procedure to that used to obtain (2.126), derive an ex-
pression for the sequential estimation of the covariance of a multivariate Gaussian
distribution, by starting with the maximum likelihood expression (2.122). Verify that
substituting the expression for a Gaussian distribution into the Robbins-Monro se-
quential estimation formula (2.135) gives a result of the same form, and hence obtain
an expression for the corresponding coefﬁcients a
N .
2.38 (⋆) Use the technique of completing the square for the quadratic form in the expo-
nent to derive the results (2.141) and (2.142).
2.39 (⋆⋆ ) Starting from the results (2.141) and (2.142) for the posterior distribution
of the mean of a Gaussian random variable, dissect out the contributions from the
ﬁrst N − 1 data points and hence obtain expressions for the sequential update of
µ
N and σ2
N . Now derive the same results starting from the posterior distribution
p(µ|x1,...,x N −1)= N(µ|µN −1,σ2
N −1) and multiplying by the likelihood func-
tion p(xN |µ)=N (xN |µ, σ2) and then completing the square and normalizing to
obtain the posterior distribution after N observations.
2.40 (⋆⋆ ) www Consider a D-dimensional Gaussian random variable x with distribu-
tion N(x|µ,Σ) in which the covarianceΣ is known and for which we wish to infer
the mean µ from a set of observationsX = {x1,..., xN }. Given a prior distribution
p(µ)=N (µ|µ0,Σ0), ﬁnd the corresponding posterior distribution p(µ|X).
2.41 (⋆) Use the deﬁnition of the gamma function (1.141) to show that the gamma dis-
tribution (2.146) is normalized.
2.42 (⋆⋆ ) Evaluate the mean, variance, and mode of the gamma distribution (2.146).
2.43 (⋆) The following distribution
p(x|σ2,q )= q
2(2σ2)1/qΓ(1/q) exp
(
− |x|q
2σ2
)
(2.293)
is a generalization of the univariate Gaussian distribution. Show that this distribution
is normalized so that ∫ ∞
−∞
p(x|σ2,q )d x =1 (2.294)
and that it reduces to the Gaussian when q =2 . Consider a regression model in
which the target variable is given by t = y(x,w)+ϵ and ϵ is a random noise


## PDF Page 154

Exercises 135
variable drawn from the distribution (2.293). Show that the log likelihood function
over w and σ2, for an observed data set of input vectors X = {x1,..., xN } and
corresponding target variables t =( t1,...,t N )T,i sg i v e nb y
ln p(t|X,w,σ2)=− 1
2σ2
N∑
n=1
|y(xn,w) − tn|q − N
q ln(2σ2)+c o n s t (2.295)
where ‘const’ denotes terms independent of both w and σ2. Note that, as a function
of w, this is the Lq error function considered in Section 1.5.5.
2.44 (⋆⋆ ) Consider a univariate Gaussian distribution N(x|µ, τ−1) having conjugate
Gaussian-gamma prior given by (2.154), and a data set x = {x1,...,x N } of i.i.d.
observations. Show that the posterior distribution is also a Gaussian-gamma distri-
bution of the same functional form as the prior, and write down expressions for the
parameters of this posterior distribution.
2.45 (⋆) Verify that the Wishart distribution deﬁned by (2.155) is indeed a conjugate
prior for the precision matrix of a multivariate Gaussian.
2.46 (⋆) www Verify that evaluating the integral in (2.158) leads to the result (2.159).
2.47 (⋆) www Show that in the limit ν →∞ , the t-distribution (2.159) becomes a
Gaussian. Hint: ignore the normalization coefﬁcient, and simply look at the depen-
dence on x.
2.48 (⋆) By following analogous steps to those used to derive the univariate Student’s
t-distribution (2.159), verify the result (2.162) for the multivariate form of the Stu-
dent’s t-distribution, by marginalizing over the variable η in (2.161). Using the
deﬁnition (2.161), show by exchanging integration variables that the multivariate
t-distribution is correctly normalized.
2.49 (⋆⋆ ) By using the deﬁnition (2.161) of the multivariate Student’s t-distribution as a
convolution of a Gaussian with a gamma distribution, verify the properties (2.164),
(2.165), and (2.166) for the multivariate t-distribution deﬁned by (2.162).
2.50 (⋆) Show that in the limit ν →∞ , the multivariate Student’s t-distribution (2.162)
reduces to a Gaussian with mean µ and precision Λ.
2.51 (⋆)
www The various trigonometric identities used in the discussion of periodic
variables in this chapter can be proven easily from the relation
exp(iA)=c o sA + isinA (2.296)
in which i is the square root of minus one. By considering the identity
exp(iA) exp(−iA)=1 (2.297)
prove the result (2.177). Similarly, using the identity
cos(A − B)=ℜ exp{i(A − B)} (2.298)


## PDF Page 155

136 2. PROBABILITY DISTRIBUTIONS
where ℜ denotes the real part, prove (2.178). Finally, by using sin(A − B)=
ℑ exp{i(A − B)}, where ℑ denotes the imaginary part, prove the result (2.183).
2.52 (⋆⋆ ) For large m, the von Mises distribution (2.179) becomes sharply peaked
around the mode θ0. By deﬁning ξ = m1/2(θ − θ0) and making the Taylor ex-
pansion of the cosine function given by
cos α =1 − α2
2 + O(α4) (2.299)
show that as m →∞ , the von Mises distribution tends to a Gaussian.
2.53 (⋆) Using the trigonometric identity (2.183), show that solution of (2.182) for θ0 is
given by (2.184).
2.54 (⋆) By computing ﬁrst and second derivatives of the von Mises distribution (2.179),
and using I0(m) > 0 for m>0, show that the maximum of the distribution occurs
when θ= θ0 and that the minimum occurs when θ= θ0 + π(mod 2π).
2.55 (⋆) By making use of the result (2.168), together with (2.184) and the trigonometric
identity (2.178), show that the maximum likelihood solutionmML for the concentra-
tion of the von Mises distribution satisﬁes A(mML)= r where r is the radius of the
mean of the observations viewed as unit vectors in the two-dimensional Euclidean
plane, as illustrated in Figure 2.17.
2.56 (⋆⋆ ) www Express the beta distribution (2.13), the gamma distribution (2.146),
and the von Mises distribution (2.179) as members of the exponential family (2.194)
and thereby identify their natural parameters.
2.57 (⋆) Verify that the multivariate Gaussian distribution can be cast in exponential
family form (2.194) and derive expressions forη, u(x), h(x) and g(η) analogous to
(2.220)–(2.223).
2.58 (⋆) The result (2.226) showed that the negative gradient oflng(η) for the exponen-
tial family is given by the expectation of u(x). By taking the second derivatives of
(2.195), show that
−∇∇ lng(η)=E[u(x)u(x) T] − E[u(x)]E[u(x)T]=c o v [u(x)]. (2.300)
2.59 (⋆) By changing variables using y = x/σ, show that the density (2.236) will be
correctly normalized, provided f(x) is correctly normalized.
2.60 (⋆⋆ ) www Consider a histogram-like density model in which the space x is di-
vided into ﬁxed regions for which the density p(x) takes the constant value hi over
the ith region, and that the volume of region i is denoted ∆ i. Suppose we have a set
of N observations of x such that ni of these observations fall in region i. Using a
Lagrange multiplier to enforce the normalization constraint on the density, derive an
expression for the maximum likelihood estimator for the {hi}.
2.61 (⋆) Show that theK-nearest-neighbour density model deﬁnes an improper distribu-
tion whose integral over all space is divergent.
