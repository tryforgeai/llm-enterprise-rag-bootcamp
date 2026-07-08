# PRML Chapter 3: Linear Models for Regression

Source: `course/week_03/data/PRML.pdf`
Book pages: 137-177
Extracted PDF pages: 156-196

> Text extracted mechanically from the local PDF for Week 04 abstractive summarization, chunking, QA-pair, and retrieval experiments.


## PDF Page 156

3
Linear
Models for
Regression
The focus so far in this book has been on unsupervised learning, including topics
such as density estimation and data clustering. We turn now to a discussion of super-
vised learning, starting with regression. The goal of regression is to predict the value
of one or more continuous target variables t given the value of aD-dimensional vec-
tor x of input variables. We have already encountered an example of a regression
problem when we considered polynomial curve ﬁtting in Chapter 1. The polynomial
is a speciﬁc example of a broad class of functions called linear regression models,
which share the property of being linear functions of the adjustable parameters, and
which will form the focus of this chapter. The simplest form of linear regression
models are also linear functions of the input variables. However, we can obtain a
much more useful class of functions by taking linear combinations of a ﬁxed set of
nonlinear functions of the input variables, known as basis functions. Such models
are linear functions of the parameters, which gives them simple analytical properties,
and yet can be nonlinear with respect to the input variables.
137


## PDF Page 157

138 3. LINEAR MODELS FOR REGRESSION
Given a training data set comprisingN observations {xn}, wheren =1 ,...,N ,
together with corresponding target values {tn}, the goal is to predict the value of t
for a new value of x. In the simplest approach, this can be done by directly con-
structing an appropriate function y(x) whose values for new inputs x constitute the
predictions for the corresponding values of t. More generally, from a probabilistic
perspective, we aim to model the predictive distributionp(t|x) because this expresses
our uncertainty about the value of t for each value of x. From this conditional dis-
tribution we can make predictions of t, for any new value of x, in such a way as to
minimize the expected value of a suitably chosen loss function. As discussed in Sec-
tion 1.5.5, a common choice of loss function for real-valued variables is the squared
loss, for which the optimal solution is given by the conditional expectation of t.
Although linear models have signiﬁcant limitations as practical techniques for
pattern recognition, particularly for problems involving input spaces of high dimen-
sionality, they have nice analytical properties and form the foundation for more so-
phisticated models to be discussed in later chapters.
3.1. Linear Basis Function Models
The simplest linear model for regression is one that involves a linear combination of
the input variables
y(x,w)=w
0 + w1x1 + ... + wDxD (3.1)
where x =( x1,...,x D)T. This is often simply known aslinear regression. The key
property of this model is that it is a linear function of the parametersw0,...,w D.I ti s
also, however, a linear function of the input variablesxi, and this imposes signiﬁcant
limitations on the model. We therefore extend the class of models by considering
linear combinations of ﬁxed nonlinear functions of the input variables, of the form
y(x,w)=w
0 +
M −1∑
j=1
wjφj(x) (3.2)
where φj(x) are known as basis functions. By denoting the maximum value of the
index j by M − 1, the total number of parameters in this model will be M.
The parameter w0 allows for any ﬁxed offset in the data and is sometimes called
a bias parameter (not to be confused with ‘bias’ in a statistical sense). It is often
convenient to deﬁne an additional dummy ‘basis function’ φ0(x)=1 so that
y(x,w)=
M −1∑
j=0
wjφj(x)= wTφ(x) (3.3)
where w =( w0,...,w M −1)T and φ =( φ0,...,φ M −1)T. In many practical ap-
plications of pattern recognition, we will apply some form of ﬁxed pre-processing,


## PDF Page 158

3.1. Linear Basis Function Models 139
or feature extraction, to the original data variables. If the original variables com-
prise the vector x, then the features can be expressed in terms of the basis functions
{φj(x)}.
By using nonlinear basis functions, we allow the function y(x,w) to be a non-
linear function of the input vector x. Functions of the form (3.2) are called linear
models, however, because this function is linear in w. It is this linearity in the pa-
rameters that will greatly simplify the analysis of this class of models. However, it
also leads to some signiﬁcant limitations, as we discuss in Section 3.6.
The example of polynomial regression considered in Chapter 1 is a particular
example of this model in which there is a single input variablex, and the basis func-
tions take the form of powers ofx so that φ
j(x)=x j . One limitation of polynomial
basis functions is that they are global functions of the input variable, so that changes
in one region of input space affect all other regions. This can be resolved by dividing
the input space up into regions and ﬁt a different polynomial in each region, leading
to spline functions (Hastie et al., 2001).
There are many other possible choices for the basis functions, for example
φ
j(x)=e x p
{
− (x − µj)2
2s2
}
(3.4)
where the µj govern the locations of the basis functions in input space, and the pa-
rameter s governs their spatial scale. These are usually referred to as ‘Gaussian’
basis functions, although it should be noted that they are not required to have a prob-
abilistic interpretation, and in particular the normalization coefﬁcient is unimportant
because these basis functions will be multiplied by adaptive parameters wj .
Another possibility is the sigmoidal basis function of the form
φj(x)=σ
(x − µj
s
)
(3.5)
where σ(a) is the logistic sigmoid function deﬁned by
σ(a)= 1
1+e x p (−a). (3.6)
Equivalently, we can use the ‘tanh’ function because this is related to the logistic
sigmoid by tanh(a)=2 σ(a) − 1, and so a general linear combination of logistic
sigmoid functions is equivalent to a general linear combination of ‘tanh’ functions.
These various choices of basis function are illustrated in Figure 3.1.
Yet another possible choice of basis function is the Fourier basis, which leads to
an expansion in sinusoidal functions. Each basis function represents a speciﬁc fre-
quency and has inﬁnite spatial extent. By contrast, basis functions that are localized
to ﬁnite regions of input space necessarily comprise a spectrum of different spatial
frequencies. In many signal processing applications, it is of interest to consider ba-
sis functions that are localized in both space and frequency, leading to a class of
functions known as wavelets. These are also deﬁned to be mutually orthogonal, to
simplify their application. Wavelets are most applicable when the input values live


## PDF Page 159

140 3. LINEAR MODELS FOR REGRESSION
−1 0 1
−1
−0.5
0
0.5
1
−1 0 1
0
0.25
0.5
0.75
1
−1 0 1
0
0.25
0.5
0.75
1
Figure 3.1 Examples of basis functions, showing polynomials on the left, Gaussians of the form (3.4) in the
centre, and sigmoidal of the form (3.5) on the right.
on a regular lattice, such as the successive time points in a temporal sequence, or the
pixels in an image. Useful texts on wavelets include Ogden (1997), Mallat (1999),
and Vidakovic (1999).
Most of the discussion in this chapter, however, is independent of the particular
choice of basis function set, and so for most of our discussion we shall not specify
the particular form of the basis functions, except for the purposes of numerical il-
lustration. Indeed, much of our discussion will be equally applicable to the situation
in which the vector φ(x) of basis functions is simply the identity φ(x)=x . Fur-
thermore, in order to keep the notation simple, we shall focus on the case of a single
target variable t. However, in Section 3.1.5, we consider brieﬂy the modiﬁcations
needed to deal with multiple target variables.
3.1.1 Maximum likelihood and least squares
In Chapter 1, we ﬁtted polynomial functions to data sets by minimizing a sum-
of-squares error function. We also showed that this error function could be motivated
as the maximum likelihood solution under an assumed Gaussian noise model. Let
us return to this discussion and consider the least squares approach, and its relation
to maximum likelihood, in more detail.
As before, we assume that the target variable t is given by a deterministic func-
tion y(x,w) with additive Gaussian noise so that
t = y(x,w)+ ϵ (3.7)
where ϵ is a zero mean Gaussian random variable with precision (inverse variance)
β. Thus we can write
p(t|x,w,β)=N (t|y(x,w),β −1). (3.8)
Recall that, if we assume a squared loss function, then the optimal prediction, for a
new value of x, will be given by the conditional mean of the target variable. In theSection 1.5.5
case of a Gaussian conditional distribution of the form (3.8), the conditional mean


## PDF Page 160

3.1. Linear Basis Function Models 141
will be simply
E[t|x]=
∫
tp(t|x)d t = y(x,w). (3.9)
Note that the Gaussian noise assumption implies that the conditional distribution of
t given x is unimodal, which may be inappropriate for some applications. An ex-
tension to mixtures of conditional Gaussian distributions, which permit multimodal
conditional distributions, will be discussed in Section 14.5.1.
Now consider a data set of inputsX = {x1,..., xN } with corresponding target
values t1,...,t N . We group the target variables {tn} into a column vector that we
denote by t where the typeface is chosen to distinguish it from a single observation
of a multivariate target, which would be denoted t. Making the assumption that
these data points are drawn independently from the distribution (3.8), we obtain the
following expression for the likelihood function, which is a function of the adjustable
parameters w and β, in the form
p(t|X,w,β)=
N∏
n=1
N(tn|wTφ(xn),β −1) (3.10)
where we have used (3.3). Note that in supervised learning problems such as regres-
sion (and classiﬁcation), we are not seeking to model the distribution of the input
variables. Thus x will always appear in the set of conditioning variables, and so
from now on we will drop the explicitx from expressions such as p(t|x,w,β) in or-
der to keep the notation uncluttered. Taking the logarithm of the likelihood function,
and making use of the standard form (1.46) for the univariate Gaussian, we have
lnp(t|w,β)=
N∑
n=1
ln N(tn|wTφ(xn),β −1)
= N
2 ln β − N
2 ln(2π) − βED(w) (3.11)
where the sum-of-squares error function is deﬁned by
ED(w)= 1
2
N∑
n=1
{tn − wTφ(xn)}2. (3.12)
Having written down the likelihood function, we can use maximum likelihood to
determine w and β. Consider ﬁrst the maximization with respect to w. As observed
already in Section 1.2.5, we see that maximization of the likelihood function under a
conditional Gaussian noise distribution for a linear model is equivalent to minimizing
a sum-of-squares error function given byED(w). The gradient of the log likelihood
function (3.11) takes the form
∇ lnp(t|w,β)=
N∑
n=1
{
tn − wTφ(xn)
}
φ(xn)T. (3.13)


## PDF Page 161

142 3. LINEAR MODELS FOR REGRESSION
Setting this gradient to zero gives
0=
N∑
n=1
tnφ(xn)T − wT
( N∑
n=1
φ(xn)φ(xn)T
)
. (3.14)
Solving for w we obtain
wML =
(
ΦTΦ
)−1
ΦTt (3.15)
which are known as thenormal equations for the least squares problem. HereΦ is an
N ×M matrix, called thedesign matrix, whose elements are given byΦnj = φj(xn),
so that
Φ =
⎛
⎜⎜⎝
φ0(x1) φ1(x1) ··· φM −1(x1)
φ0(x2) φ1(x2) ··· φM −1(x2)
... ... ... ...
φ0(xN ) φ1(xN ) ··· φM −1(xN )
⎞
⎟⎟⎠ . (3.16)
The quantity
Φ† ≡
(
ΦTΦ
)−1
ΦT (3.17)
is known as the Moore-Penrose pseudo-inverse of the matrix Φ (Rao and Mitra,
1971; Golub and Van Loan, 1996). It can be regarded as a generalization of the
notion of matrix inverse to nonsquare matrices. Indeed, ifΦ is square and invertible,
then using the property (AB)−1 = B−1A−1 we see that Φ† ≡ Φ−1.
At this point, we can gain some insight into the role of the bias parameterw0.I f
we make the bias parameter explicit, then the error function (3.12) becomes
ED(w)= 1
2
N∑
n=1
{tn − w0 −
M −1∑
j=1
wjφj(xn)}2. (3.18)
Setting the derivative with respect tow0 equal to zero, and solving forw0, we obtain
w0 = t −
M −1∑
j=1
wjφj (3.19)
where we have deﬁned
t = 1
N
N∑
n=1
tn, φj = 1
N
N∑
n=1
φj(xn). (3.20)
Thus the bias w0 compensates for the difference between the averages (over the
training set) of the target values and the weighted sum of the averages of the basis
function values.
We can also maximize the log likelihood function (3.11) with respect to the noise
precision parameter β, giving
1
βML
= 1
N
N∑
n=1
{tn − wT
MLφ(xn)}2 (3.21)


## PDF Page 162

3.1. Linear Basis Function Models 143
Figure 3.2 Geometrical interpretation of the least-squares
solution, in anN-dimensional space whose axes
are the values of t1,...,t N . The least-squares
regression function is obtained by ﬁnding the or-
thogonal projection of the data vector t onto the
subspace spanned by the basis functions φ
j(x)
in which each basis function is viewed as a vec-
tor ϕ
j of length N with elements φj(xn).
S
t
yϕ1
ϕ2
and so we see that the inverse of the noise precision is given by the residual variance
of the target values around the regression function.
3.1.2 Geometry of least squares
At this point, it is instructive to consider the geometrical interpretation of the
least-squares solution. To do this we consider an N-dimensional space whose axes
are given by the tn, so that t =( t1,...,t N )T is a vector in this space. Each basis
function φj(xn), evaluated at theN data points, can also be represented as a vector in
the same space, denoted byϕj, as illustrated in Figure 3.2. Note thatϕj corresponds
to the jth column of Φ, whereas φ(xn) corresponds to the nth row of Φ. If the
number M of basis functions is smaller than the number N of data points, then the
M vectors φj(xn) will span a linear subspace S of dimensionality M. We deﬁne
y to be an N-dimensional vector whose nth element is given by y(xn,w), where
n =1 ,...,N . Because y is an arbitrary linear combination of the vectors ϕj , it can
live anywhere in the M-dimensional subspace. The sum-of-squares error (3.12) is
then equal (up to a factor of 1/2) to the squared Euclidean distance between y and
t. Thus the least-squares solution for w corresponds to that choice of y that lies in
subspace S and that is closest to t. Intuitively, from Figure 3.2, we anticipate that
this solution corresponds to the orthogonal projection of t onto the subspace S. This
is indeed the case, as can easily be veriﬁed by noting that the solution for y is given
by ΦwML, and then conﬁrming that this takes the form of an orthogonal projection.Exercise 3.2
In practice, a direct solution of the normal equations can lead to numerical difﬁ-
culties when ΦTΦ is close to singular. In particular, when two or more of the basis
vectors ϕj are co-linear, or nearly so, the resulting parameter values can have large
magnitudes. Such near degeneracies will not be uncommon when dealing with real
data sets. The resulting numerical difﬁculties can be addressed using the technique
of singular value decomposition ,o r SVD (Press et al. , 1992; Bishop and Nabney,
2008). Note that the addition of a regularization term ensures that the matrix is non-
singular, even in the presence of degeneracies.
3.1.3 Sequential learning
Batch techniques, such as the maximum likelihood solution (3.15), which in-
volve processing the entire training set in one go, can be computationally costly for
large data sets. As we have discussed in Chapter 1, if the data set is sufﬁciently large,
it may be worthwhile to usesequential algorithms, also known ason-line algorithms,


## PDF Page 163

144 3. LINEAR MODELS FOR REGRESSION
in which the data points are considered one at a time, and the model parameters up-
dated after each such presentation. Sequential learning is also appropriate for real-
time applications in which the data observations are arriving in a continuous stream,
and predictions must be made before all of the data points are seen.
We can obtain a sequential learning algorithm by applying the technique of
stochastic gradient descent, also known assequential gradient descent, as follows. If
the error function comprises a sum over data points E =
∑
n En, then after presen-
tation of pattern n, the stochastic gradient descent algorithm updates the parameter
vector w using
w(τ+1) = w(τ) − η∇En (3.22)
where τ denotes the iteration number, and η is a learning rate parameter. We shall
discuss the choice of value forηshortly. The value ofw is initialized to some starting
vector w(0). For the case of the sum-of-squares error function (3.12), this gives
w(τ+1) = w(τ) + η(tn − w(τ)Tφn)φn (3.23)
where φn = φ(xn). This is known as least-mean-squares or the LMS algorithm.
The value of η needs to be chosen with care to ensure that the algorithm converges
(Bishop and Nabney, 2008).
3.1.4 Regularized least squares
In Section 1.1, we introduced the idea of adding a regularization term to an
error function in order to control over-ﬁtting, so that the total error function to be
minimized takes the form
E
D(w)+ λEW (w) (3.24)
where λ is the regularization coefﬁcient that controls the relative importance of the
data-dependent error ED(w) and the regularization term EW (w). One of the sim-
plest forms of regularizer is given by the sum-of-squares of the weight vector ele-
ments
E
W (w)= 1
2wTw. (3.25)
If we also consider the sum-of-squares error function given by
E(w)= 1
2
N∑
n=1
{tn − wTφ(xn)}2 (3.26)
then the total error function becomes
1
2
N∑
n=1
{tn − wTφ(xn)}2 + λ
2wTw. (3.27)
This particular choice of regularizer is known in the machine learning literature as
weight decay because in sequential learning algorithms, it encourages weight values
to decay towards zero, unless supported by the data. In statistics, it provides an ex-
ample of a parameter shrinkage method because it shrinks parameter values towards


## PDF Page 164

3.1. Linear Basis Function Models 145
q =0 .5 q =1 q =2 q =4
Figure 3.3 Contours of the regularization term in (3.29) for various values of the parameter q.
zero. It has the advantage that the error function remains a quadratic function of
w, and so its exact minimizer can be found in closed form. Speciﬁcally, setting the
gradient of (3.27) with respect to w to zero, and solving for w as before, we obtain
w =
(
λI+ ΦTΦ
)−1
ΦTt. (3.28)
This represents a simple extension of the least-squares solution (3.15).
A more general regularizer is sometimes used, for which the regularized error
takes the form
1
2
N∑
n=1
{tn − wTφ(xn)}2 + λ
2
M∑
j=1
|wj |q (3.29)
where q =2 corresponds to the quadratic regularizer (3.27). Figure 3.3 shows con-
tours of the regularization function for different values of q.
The case of q =1 is know as the lasso in the statistics literature (Tibshirani,
1996). It has the property that if λ is sufﬁciently large, some of the coefﬁcients
wj are driven to zero, leading to a sparse model in which the corresponding basis
functions play no role. To see this, we ﬁrst note that minimizing (3.29) is equivalent
to minimizing the unregularized sum-of-squares error (3.12) subject to the constraintExercise 3.5
M∑
j=1
|wj |q ⩽ η (3.30)
for an appropriate value of the parameterη, where the two approaches can be related
using Lagrange multipliers. The origin of the sparsity can be seen from Figure 3.4,Appendix E
which shows that the minimum of the error function, subject to the constraint (3.30).
As λ is increased, so an increasing number of parameters are driven to zero.
Regularization allows complex models to be trained on data sets of limited size
without severe over-ﬁtting, essentially by limiting the effective model complexity.
However, the problem of determining the optimal model complexity is then shifted
from one of ﬁnding the appropriate number of basis functions to one of determining
a suitable value of the regularization coefﬁcient λ. We shall return to the issue of
model complexity later in this chapter.


## PDF Page 165

146 3. LINEAR MODELS FOR REGRESSION
Figure 3.4 Plot of the contours
of the unregularized error function
(blue) along with the constraint re-
gion (3.30) for the quadratic regular-
izer q =2 on the left and the lasso
regularizer q =1 on the right, in
which the optimum value for the pa-
rameter vector w is denoted by w
⋆.
The lasso gives a sparse solution in
which w
⋆
1 =0 .
w1
w2
w⋆
w1
w2
w⋆
For the remainder of this chapter we shall focus on the quadratic regularizer
(3.27) both for its practical importance and its analytical tractability.
3.1.5 Multiple outputs
So far, we have considered the case of a single target variablet. In some applica-
tions, we may wish to predict K> 1 target variables, which we denote collectively
by the target vectort. This could be done by introducing a different set of basis func-
tions for each component oft, leading to multiple, independent regression problems.
However, a more interesting, and more common, approach is to use the same set of
basis functions to model all of the components of the target vector so that
y(x,w)=W Tφ(x) (3.31)
where y is a K-dimensional column vector, W is an M × K matrix of parameters,
and φ(x) is an M-dimensional column vector with elements φj(x), with φ0(x)=1
as before. Suppose we take the conditional distribution of the target vector to be an
isotropic Gaussian of the form
p(t|x,W,β)=N (t|WTφ(x),β −1I). (3.32)
If we have a set of observations t1,..., tN , we can combine these into a matrix T
of size N × K such that the nth row is given by tT
n . Similarly, we can combine the
input vectors x1,..., xN into a matrix X. The log likelihood function is then given
by
lnp(T|X,W,β)=
N∑
n=1
ln N(tn|WTφ(xn),β −1I)
= NK
2 ln
( β
2π
)
− β
2
N∑
n=1
tn − WTφ(xn)


2
. (3.33)


## PDF Page 166

3.2. The Bias-Variance Decomposition 147
As before, we can maximize this function with respect to W, giving
WML =
(
ΦTΦ
)−1
ΦTT. (3.34)
If we examine this result for each target variable tk,w eh a v e
wk =
(
ΦTΦ
)−1
ΦTtk = Φ†tk (3.35)
where tk is an N-dimensional column vector with componentstnk for n =1 ,...N .
Thus the solution to the regression problem decouples between the different target
variables, and we need only compute a single pseudo-inverse matrix Φ†, which is
shared by all of the vectors wk.
The extension to general Gaussian noise distributions having arbitrary covari-
ance matrices is straightforward. Again, this leads to a decoupling into K inde-Exercise 3.6
pendent regression problems. This result is unsurprising because the parameters W
deﬁne only the mean of the Gaussian noise distribution, and we know from Sec-
tion 2.3.4 that the maximum likelihood solution for the mean of a multivariate Gaus-
sian is independent of the covariance. From now on, we shall therefore consider a
single target variable t for simplicity.
3.2. The Bias-Variance Decomposition
So far in our discussion of linear models for regression, we have assumed that the
form and number of basis functions are both ﬁxed. As we have seen in Chapter 1,
the use of maximum likelihood, or equivalently least squares, can lead to severe
over-ﬁtting if complex models are trained using data sets of limited size. However,
limiting the number of basis functions in order to avoid over-ﬁtting has the side
effect of limiting the ﬂexibility of the model to capture interesting and important
trends in the data. Although the introduction of regularization terms can control
over-ﬁtting for models with many parameters, this raises the question of how to
determine a suitable value for the regularization coefﬁcient λ. Seeking the solution
that minimizes the regularized error function with respect to both the weight vector
w and the regularization coefﬁcient λ is clearly not the right approach since this
leads to the unregularized solution with λ =0 .
As we have seen in earlier chapters, the phenomenon of over-ﬁtting is really an
unfortunate property of maximum likelihood and does not arise when we marginalize
over parameters in a Bayesian setting. In this chapter, we shall consider the Bayesian
view of model complexity in some depth. Before doing so, however, it is instructive
to consider a frequentist viewpoint of the model complexity issue, known as thebias-
variance trade-off. Although we shall introduce this concept in the context of linear
basis function models, where it is easy to illustrate the ideas using simple examples,
the discussion has more general applicability.
In Section 1.5.5, when we discussed decision theory for regression problems,
we considered various loss functions each of which leads to a corresponding optimal
prediction once we are given the conditional distributionp(t|x). A popular choice is


## PDF Page 167

148 3. LINEAR MODELS FOR REGRESSION
the squared loss function, for which the optimal prediction is given by the conditional
expectation, which we denote by h(x) and which is given by
h(x)=E[t|x]=
∫
tp(t|x)d t. (3.36)
At this point, it is worth distinguishing between the squared loss function arising
from decision theory and the sum-of-squares error function that arose in the maxi-
mum likelihood estimation of model parameters. We might use more sophisticated
techniques than least squares, for example regularization or a fully Bayesian ap-
proach, to determine the conditional distribution p(t|x). These can all be combined
with the squared loss function for the purpose of making predictions.
We showed in Section 1.5.5 that the expected squared loss can be written in the
form
E[L]=
∫
{y(x) − h(x)}2 p(x)dx +
∫
{h(x) − t}2p(x,t )dxdt. (3.37)
Recall that the second term, which is independent of y(x), arises from the intrinsic
noise on the data and represents the minimum achievable value of the expected loss.
The ﬁrst term depends on our choice for the function y(x), and we will seek a so-
lution for y(x) which makes this term a minimum. Because it is nonnegative, the
smallest that we can hope to make this term is zero. If we had an unlimited supply of
data (and unlimited computational resources), we could in principle ﬁnd the regres-
sion function h(x) to any desired degree of accuracy, and this would represent the
optimal choice for y(x). However, in practice we have a data set D containing only
a ﬁnite number N of data points, and consequently we do not know the regression
function h(x) exactly.
If we model the h(x) using a parametric function y(x,w) governed by a pa-
rameter vector w, then from a Bayesian perspective the uncertainty in our model is
expressed through a posterior distribution overw. A frequentist treatment, however,
involves making a point estimate of w based on the data set D, and tries instead
to interpret the uncertainty of this estimate through the following thought experi-
ment. Suppose we had a large number of data sets each of size N and each drawn
independently from the distribution p(t,x). For any given data set D, we can run
our learning algorithm and obtain a prediction function y(x; D). Different data sets
from the ensemble will give different functions and consequently different values of
the squared loss. The performance of a particular learning algorithm is then assessed
by taking the average over this ensemble of data sets.
Consider the integrand of the ﬁrst term in (3.37), which for a particular data set
D takes the form
{y(x; D) − h(x)}2. (3.38)
Because this quantity will be dependent on the particular data setD, we take its aver-
age over the ensemble of data sets. If we add and subtract the quantity ED[y(x; D)]


## PDF Page 168

3.2. The Bias-Variance Decomposition 149
inside the braces, and then expand, we obtain
{y(x; D) − ED[y(x; D)] + ED[y(x; D)] − h(x)}2
= {y(x; D) − ED[y(x; D)]}2 + {ED[y(x; D)] − h(x)}2
+2{y(x; D) − ED[y(x; D)]}{ED[y(x; D)] − h(x)}. (3.39)
We now take the expectation of this expression with respect to D and note that the
ﬁnal term will vanish, giving
ED
[
{y(x; D) − h(x)}2]
= {ED[y(x; D)] − h(x)}2
  
(bias)2
+ ED
[
{y(x; D) − ED[y(x; D)]}2]
  
variance
. (3.40)
We see that the expected squared difference between y(x; D) and the regression
function h(x) can be expressed as the sum of two terms. The ﬁrst term, called the
squared bias, represents the extent to which the average prediction over all data sets
differs from the desired regression function. The second term, called the variance,
measures the extent to which the solutions for individual data sets vary around their
average, and hence this measures the extent to which the functiony(x; D) is sensitive
to the particular choice of data set. We shall provide some intuition to support these
deﬁnitions shortly when we consider a simple example.
So far, we have considered a single input valuex. If we substitute this expansion
back into (3.37), we obtain the following decomposition of the expected squared loss
expected loss =( bias)2 + variance + noise (3.41)
where
(bias)2 =
∫
{ED[y(x; D)] − h(x)}2p(x)dx (3.42)
variance =
∫
ED
[
{y(x; D) − ED[y(x; D)]}2]
p(x)dx (3.43)
noise =
∫
{h(x) − t}2p(x,t )dxdt (3.44)
and the bias and variance terms now refer to integrated quantities.
Our goal is to minimize the expected loss, which we have decomposed into the
sum of a (squared) bias, a variance, and a constant noise term. As we shall see, there
is a trade-off between bias and variance, with very ﬂexible models having low bias
and high variance, and relatively rigid models having high bias and low variance.
The model with the optimal predictive capability is the one that leads to the best
balance between bias and variance. This is illustrated by considering the sinusoidal
data set from Chapter 1. Here we generate 100 data sets, each containing N =2 5Appendix A
data points, independently from the sinusoidal curve h(x)=s i n ( 2πx). The data
sets are indexed by l =1 ,...,L , where L = 100, and for each data set D
(l) we


## PDF Page 169

150 3. LINEAR MODELS FOR REGRESSION
x
t
lnλ =2 .6
0 1
−1
0
1
x
t
0 1
−1
0
1
x
t
lnλ = −0.31
0 1
−1
0
1
x
t
0 1
−1
0
1
x
t
lnλ = −2.4
0 1
−1
0
1
x
t
0 1
−1
0
1
Figure 3.5 Illustration of the dependence of bias and variance on model complexity, governed by a regulariza-
tion parameterλ, using the sinusoidal data set from Chapter 1. There areL = 100 data sets, each havingN =2 5
data points, and there are 24 Gaussian basis functions in the model so that the total number of parameters is
M =2 5 including the bias parameter. The left column shows the result of ﬁtting the model to the data sets for
various values of ln λ (for clarity, only 20 of the 100 ﬁts are shown). The right column shows the corresponding
average of the 100 ﬁts (red) along with the sinusoidal function from which the data sets were generated (green).


## PDF Page 170

3.2. The Bias-Variance Decomposition 151
Figure 3.6 Plot of squared bias and variance,
together with their sum, correspond-
ing to the results shown in Fig-
ure 3.5. Also shown is the average
test set error for a test data set size
of 1000 points. The minimum value
of (bias)
2 + variance occurs around
ln λ = −0.31, which is close to the
value that gives the minimum error
on the test data.
lnλ
−3 −2 −1 0 1 2
0
0.03
0.06
0.09
0.12
0.15
(bias)2
variance
(bias)2 + variance
test error
ﬁt a model with 24 Gaussian basis functions by minimizing the regularized error
function (3.27) to give a prediction function y(l)(x) as shown in Figure 3.5. The
top row corresponds to a large value of the regularization coefﬁcient λ that gives low
variance (because the red curves in the left plot look similar) but high bias (because
the two curves in the right plot are very different). Conversely on the bottom row, for
which λ is small, there is large variance (shown by the high variability between the
red curves in the left plot) but low bias (shown by the good ﬁt between the average
model ﬁt and the original sinusoidal function). Note that the result of averaging many
solutions for the complex model with M =2 5 is a very good ﬁt to the regression
function, which suggests that averaging may be a beneﬁcial procedure. Indeed, a
weighted averaging of multiple solutions lies at the heart of a Bayesian approach,
although the averaging is with respect to the posterior distribution of parameters, not
with respect to multiple data sets.
We can also examine the bias-variance trade-off quantitatively for this example.
The average prediction is estimated from
y(x)= 1
L
L∑
l=1
y(l)(x) (3.45)
and the integrated squared bias and integrated variance are then given by
(bias)2 = 1
N
N∑
n=1
{y(xn) − h(xn)}2 (3.46)
variance = 1
N
N∑
n=1
1
L
L∑
l=1
{
y(l)(xn) − y(xn)
}2
(3.47)
where the integral over x weighted by the distribution p(x) is approximated by a
ﬁnite sum over data points drawn from that distribution. These quantities, along
with their sum, are plotted as a function of lnλ in Figure 3.6. We see that small
values of λ allow the model to become ﬁnely tuned to the noise on each individual


## PDF Page 171

152 3. LINEAR MODELS FOR REGRESSION
data set leading to large variance. Conversely, a large value of λ pulls the weight
parameters towards zero leading to large bias.
Although the bias-variance decomposition may provide some interesting in-
sights into the model complexity issue from a frequentist perspective, it is of lim-
ited practical value, because the bias-variance decomposition is based on averages
with respect to ensembles of data sets, whereas in practice we have only the single
observed data set. If we had a large number of independent training sets of a given
size, we would be better off combining them into a single large training set, which
of course would reduce the level of over-ﬁtting for a given model complexity.
Given these limitations, we turn in the next section to a Bayesian treatment of
linear basis function models, which not only provides powerful insights into the
issues of over-ﬁtting but which also leads to practical techniques for addressing the
question model complexity.
3.3. Bayesian Linear Regression
In our discussion of maximum likelihood for setting the parameters of a linear re-
gression model, we have seen that the effective model complexity, governed by the
number of basis functions, needs to be controlled according to the size of the data
set. Adding a regularization term to the log likelihood function means the effective
model complexity can then be controlled by the value of the regularization coefﬁ-
cient, although the choice of the number and form of the basis functions is of course
still important in determining the overall behaviour of the model.
This leaves the issue of deciding the appropriate model complexity for the par-
ticular problem, which cannot be decided simply by maximizing the likelihood func-
tion, because this always leads to excessively complex models and over-ﬁtting. In-
dependent hold-out data can be used to determine model complexity, as discussed
in Section 1.3, but this can be both computationally expensive and wasteful of valu-
able data. We therefore turn to a Bayesian treatment of linear regression, which will
avoid the over-ﬁtting problem of maximum likelihood, and which will also lead to
automatic methods of determining model complexity using the training data alone.
Again, for simplicity we will focus on the case of a single target variable t. Ex-
tension to multiple target variables is straightforward and follows the discussion of
Section 3.1.5.
3.3.1 Parameter distribution
We begin our discussion of the Bayesian treatment of linear regression by in-
troducing a prior probability distribution over the model parameters w. For the mo-
ment, we shall treat the noise precision parameter β as a known constant. First note
that the likelihood functionp(t|w) deﬁned by (3.10) is the exponential of a quadratic
function of w. The corresponding conjugate prior is therefore given by a Gaussian
distribution of the form
p(w)=N (w|m0,S0) (3.48)
having mean m0 and covariance S0.


## PDF Page 172

3.3. Bayesian Linear Regression 153
Next we compute the posterior distribution, which is proportional to the product
of the likelihood function and the prior. Due to the choice of a conjugate Gaus-
sian prior distribution, the posterior will also be Gaussian. We can evaluate this
distribution by the usual procedure of completing the square in the exponential, and
then ﬁnding the normalization coefﬁcient using the standard result for a normalized
Gaussian. However, we have already done the necessary work in deriving the gen-Exercise 3.7
eral result (2.116), which allows us to write down the posterior distribution directly
in the form
p(w|t)=N (w|m
N ,SN ) (3.49)
where
mN = SN
(
S−1
0 m0 + βΦTt
)
(3.50)
S−1
N = S−1
0 + βΦTΦ. (3.51)
Note that because the posterior distribution is Gaussian, its mode coincides with its
mean. Thus the maximum posterior weight vector is simply given byw
MAP = mN .
If we consider an inﬁnitely broad prior S0 = α−1I with α → 0, the mean mN
of the posterior distribution reduces to the maximum likelihood value wML given
by (3.15). Similarly, if N =0 , then the posterior distribution reverts to the prior.
Furthermore, if data points arrive sequentially, then the posterior distribution at any
stage acts as the prior distribution for the subsequent data point, such that the new
posterior distribution is again given by (3.49).Exercise 3.8
For the remainder of this chapter, we shall consider a particular form of Gaus-
sian prior in order to simplify the treatment. Speciﬁcally, we consider a zero-mean
isotropic Gaussian governed by a single precision parameter α so that
p(w|α)=N (w|0,α
−1I) (3.52)
and the corresponding posterior distribution over w is then given by (3.49) with
mN = βSNΦTt (3.53)
S−1
N = αI + βΦTΦ. (3.54)
The log of the posterior distribution is given by the sum of the log likelihood and
the log of the prior and, as a function of w, takes the form
lnp(w|t)= − β
2
N∑
n=1
{tn − wTφ(xn)}2 − α
2wTw +c o n s t. (3.55)
Maximization of this posterior distribution with respect to w is therefore equiva-
lent to the minimization of the sum-of-squares error function with the addition of a
quadratic regularization term, corresponding to (3.27) with λ = α/β.
We can illustrate Bayesian learning in a linear basis function model, as well as
the sequential update of a posterior distribution, using a simple example involving
straight-line ﬁtting. Consider a single input variable x, a single target variable t and


## PDF Page 173

154 3. LINEAR MODELS FOR REGRESSION
a linear model of the form y(x,w)= w0 + w1x. Because this has just two adap-
tive parameters, we can plot the prior and posterior distributions directly in parameter
space. We generate synthetic data from the functionf(x,a)=a 0 +a1x with param-
eter values a0 = −0.3 and a1 =0 .5 by ﬁrst choosing values of xn from the uniform
distribution U(x|− 1, 1), then evaluatingf(xn,a), and ﬁnally adding Gaussian noise
with standard deviation of 0.2 to obtain the target values tn. Our goal is to recover
the values of a0 and a1 from such data, and we will explore the dependence on the
size of the data set. We assume here that the noise variance is known and hence we
set the precision parameter to its true value β =( 1/0.2)
2 =2 5. Similarly, we ﬁx
the parameter α to 2.0. We shall shortly discuss strategies for determining α and
β from the training data. Figure 3.7 shows the results of Bayesian learning in this
model as the size of the data set is increased and demonstrates the sequential nature
of Bayesian learning in which the current posterior distribution forms the prior when
a new data point is observed. It is worth taking time to study this ﬁgure in detail as
it illustrates several important aspects of Bayesian inference. The ﬁrst row of this
ﬁgure corresponds to the situation before any data points are observed and shows a
plot of the prior distribution in w space together with six samples of the function
y(x,w) in which the values of w are drawn from the prior. In the second row, we
see the situation after observing a single data point. The location (x, t) of the data
point is shown by a blue circle in the right-hand column. In the left-hand column is a
plot of the likelihood function p(t|x,w) for this data point as a function of w. Note
that the likelihood function provides a soft constraint that the line must pass close to
the data point, where close is determined by the noise precision β. For comparison,
the true parameter values a
0 = −0.3 and a1 =0 .5 used to generate the data set
are shown by a white cross in the plots in the left column of Figure 3.7. When we
multiply this likelihood function by the prior from the top row, and normalize, we
obtain the posterior distribution shown in the middle plot on the second row. Sam-
ples of the regression function y(x,w) obtained by drawing samples of w from this
posterior distribution are shown in the right-hand plot. Note that these sample lines
all pass close to the data point. The third row of this ﬁgure shows the effect of ob-
serving a second data point, again shown by a blue circle in the plot in the right-hand
column. The corresponding likelihood function for this second data point alone is
shown in the left plot. When we multiply this likelihood function by the posterior
distribution from the second row, we obtain the posterior distribution shown in the
middle plot of the third row. Note that this is exactly the same posterior distribution
as would be obtained by combining the original prior with the likelihood function
for the two data points. This posterior has now been inﬂuenced by two data points,
and because two points are sufﬁcient to deﬁne a line this already gives a relatively
compact posterior distribution. Samples from this posterior distribution give rise to
the functions shown in red in the third column, and we see that these functions pass
close to both of the data points. The fourth row shows the effect of observing a total
of 20 data points. The left-hand plot shows the likelihood function for the 20
th data
point alone, and the middle plot shows the resulting posterior distribution that has
now absorbed information from all 20 observations. Note how the posterior is much
sharper than in the third row. In the limit of an inﬁnite number of data points, the


## PDF Page 174

3.3. Bayesian Linear Regression 155
Figure 3.7 Illustration of sequential Bayesian learning for a simple linear model of the formy(x,w)=
w0 + w1x. A detailed description of this ﬁgure is given in the text.


## PDF Page 175

156 3. LINEAR MODELS FOR REGRESSION
posterior distribution would become a delta function centred on the true parameter
values, shown by the white cross.
Other forms of prior over the parameters can be considered. For instance, we
can generalize the Gaussian prior to give
p(w|α)=
[ q
2
(α
2
)1/q 1
Γ(1/q)
]M
exp
(
− α
2
M∑
j=1
|wj |q
)
(3.56)
in which q =2 corresponds to the Gaussian distribution, and only in this case is the
prior conjugate to the likelihood function (3.10). Finding the maximum of the poste-
rior distribution overw corresponds to minimization of the regularized error function
(3.29). In the case of the Gaussian prior, the mode of the posterior distribution was
equal to the mean, although this will no longer hold if q ̸=2 .
3.3.2 Predictive distribution
In practice, we are not usually interested in the value of w itself but rather in
making predictions of t for new values of x. This requires that we evaluate the
predictive distribution deﬁned by
p(t|t,α ,β)=
∫
p(t|w,β)p(w|t,α ,β)dw (3.57)
in which t is the vector of target values from the training set, and we have omitted the
corresponding input vectors from the right-hand side of the conditioning statements
to simplify the notation. The conditional distribution p(t|x,w,β) of the target vari-
able is given by (3.8), and the posterior weight distribution is given by (3.49). We
see that (3.57) involves the convolution of two Gaussian distributions, and so making
use of the result (2.115) from Section 8.1.4, we see that the predictive distribution
takes the formExercise 3.10
p(t|x, t,α ,β)= N(t|m
T
N φ(x),σ2
N (x)) (3.58)
where the variance σ2
N (x) of the predictive distribution is given by
σ2
N (x)= 1
β + φ(x)TSN φ(x). (3.59)
The ﬁrst term in (3.59) represents the noise on the data whereas the second term
reﬂects the uncertainty associated with the parameters w. Because the noise process
and the distribution of w are independent Gaussians, their variances are additive.
Note that, as additional data points are observed, the posterior distribution becomes
narrower. As a consequence it can be shown (Qazaz et al., 1997) that σ
2
N+1(x) ⩽
σ2
N (x). In the limit N →∞ , the second term in (3.59) goes to zero, and the varianceExercise 3.11
of the predictive distribution arises solely from the additive noise governed by the
parameter β.
As an illustration of the predictive distribution for Bayesian linear regression
models, let us return to the synthetic sinusoidal data set of Section 1.1. In Figure 3.8,


## PDF Page 176

3.3. Bayesian Linear Regression 157
x
t
0 1
−1
0
1
x
t
0 1
−1
0
1
x
t
0 1
−1
0
1
x
t
0 1
−1
0
1
Figure 3.8 Examples of the predictive distribution (3.58) for a model consisting of 9 Gaussian basis functions
of the form (3.4) using the synthetic sinusoidal data set of Section 1.1. See the text for a detailed discussion.
we ﬁt a model comprising a linear combination of Gaussian basis functions to data
sets of various sizes and then look at the corresponding posterior distributions. Here
the green curves correspond to the function sin(2πx) from which the data points
were generated (with the addition of Gaussian noise). Data sets of size N =1 ,
N =2 , N =4 , and N =2 5 are shown in the four plots by the blue circles. For
each plot, the red curve shows the mean of the corresponding Gaussian predictive
distribution, and the red shaded region spans one standard deviation either side of
the mean. Note that the predictive uncertainty depends on x and is smallest in the
neighbourhood of the data points. Also note that the level of uncertainty decreases
as more data points are observed.
The plots in Figure 3.8 only show the point-wise predictive variance as a func-
tion of x. In order to gain insight into the covariance between the predictions at
different values of x, we can draw samples from the posterior distribution over w,
and then plot the corresponding functions y(x,w), as shown in Figure 3.9.


## PDF Page 177

158 3. LINEAR MODELS FOR REGRESSION
x
t
0 1
−1
0
1
x
t
0 1
−1
0
1
x
t
0 1
−1
0
1
x
t
0 1
−1
0
1
Figure 3.9 Plots of the function y(x,w) using samples from the posterior distributions overw corresponding to
the plots in Figure 3.8.
If we used localized basis functions such as Gaussians, then in regions away
from the basis function centres, the contribution from the second term in the predic-
tive variance (3.59) will go to zero, leaving only the noise contribution β−1. Thus,
the model becomes very conﬁdent in its predictions when extrapolating outside the
region occupied by the basis functions, which is generally an undesirable behaviour.
This problem can be avoided by adopting an alternative Bayesian approach to re-
gression known as a Gaussian process.Section 6.4
Note that, if both w and β are treated as unknown, then we can introduce a
conjugate prior distribution p(w,β) that, from the discussion in Section 2.3.6, will
be given by a Gaussian-gamma distribution (Denison et al., 2002). In this case, theExercise 3.12
predictive distribution is a Student’s t-distribution.Exercise 3.13


## PDF Page 178

3.3. Bayesian Linear Regression 159
Figure 3.10 The equivalent ker-
nel k(x, x′) for the Gaussian basis
functions in Figure 3.1, shown as
a plot of x versus x′, together with
three slices through this matrix cor-
responding to three different values
of x. The data set used to generate
this kernel comprised 200 values of
x equally spaced over the interval
(−1, 1).
3.3.3 Equivalent kernel
The posterior mean solution (3.53) for the linear basis function model has an in-
teresting interpretation that will set the stage for kernel methods, including Gaussian
processes. If we substitute (3.53) into the expression (3.3), we see that the predictiveChapter 6
mean can be written in the form
y(x,mN )=m T
N φ(x)=β φ(x)TSNΦTt =
N∑
n=1
βφ(x)TSN φ(xn)tn (3.60)
where SN is deﬁned by (3.51). Thus the mean of the predictive distribution at a point
x is given by a linear combination of the training set target variables tn, so that we
can write
y(x,mN )=
N∑
n=1
k(x,xn)tn (3.61)
where the function
k(x,x′)=β φ(x)TSN φ(x′) (3.62)
is known as thesmoother matrix or the equivalent kernel. Regression functions, such
as this, which make predictions by taking linear combinations of the training set
target values are known aslinear smoothers. Note that the equivalent kernel depends
on the input values xn from the data set because these appear in the deﬁnition of
SN . The equivalent kernel is illustrated for the case of Gaussian basis functions in
Figure 3.10 in which the kernel functions k(x, x′) have been plotted as a function of
x′ for three different values ofx. We see that they are localized aroundx, and so the
mean of the predictive distribution at x, given by y(x,mN ), is obtained by forming
a weighted combination of the target values in which data points close tox are given
higher weight than points further removed from x. Intuitively, it seems reasonable
that we should weight local evidence more strongly than distant evidence. Note that
this localization property holds not only for the localized Gaussian basis functions
but also for the nonlocal polynomial and sigmoidal basis functions, as illustrated in
Figure 3.11.


## PDF Page 179

160 3. LINEAR MODELS FOR REGRESSION
Figure 3.11 Examples of equiva-
lent kernels k(x, x′) for x =0
plotted as a function of x′, corre-
sponding (left) to the polynomial ba-
sis functions and (right) to the sig-
moidal basis functions shown in Fig-
ure 3.1. Note that these are local-
ized functions of x
′ even though the
corresponding basis functions are
nonlocal.
−1 0 1
0
0.02
0.04
−1 0 1
0
0.02
0.04
Further insight into the role of the equivalent kernel can be obtained by consid-
ering the covariance between y(x) and y(x′), which is given by
cov[y(x),y (x′) ]=c o v [ φ(x)Tw,wTφ(x′)]
= φ(x)TSN φ(x′)= β−1k(x,x′) (3.63)
where we have made use of (3.49) and (3.62). From the form of the equivalent
kernel, we see that the predictive mean at nearby points will be highly correlated,
whereas for more distant pairs of points the correlation will be smaller.
The predictive distribution shown in Figure 3.8 allows us to visualize the point-
wise uncertainty in the predictions, governed by (3.59). However, by drawing sam-
ples from the posterior distribution over w, and plotting the corresponding model
functions y(x,w) as in Figure 3.9, we are visualizing the joint uncertainty in the
posterior distribution between they values at two (or more)x values, as governed by
the equivalent kernel.
The formulation of linear regression in terms of a kernel function suggests an
alternative approach to regression as follows. Instead of introducing a set of basis
functions, which implicitly determines an equivalent kernel, we can instead deﬁne
a localized kernel directly and use this to make predictions for new input vectors x,
given the observed training set. This leads to a practical framework for regression
(and classiﬁcation) called Gaussian processes, which will be discussed in detail in
Section 6.4.
We have seen that the effective kernel deﬁnes the weights by which the training
set target values are combined in order to make a prediction at a new value ofx, and
it can be shown that these weights sum to one, in other words
N∑
n=1
k(x,xn)=1 (3.64)
for all values of x. This intuitively pleasing result can easily be proven informallyExercise 3.14
by noting that the summation is equivalent to considering the predictive mean ˆy(x)
for a set of target data in which tn =1 for all n. Provided the basis functions are
linearly independent, that there are more data points than basis functions, and that
one of the basis functions is constant (corresponding to the bias parameter), then it is
clear that we can ﬁt the training data exactly and hence that the predictive mean will


## PDF Page 180

3.4. Bayesian Model Comparison 161
be simply ˆy(x)=1 , from which we obtain (3.64). Note that the kernel function can
be negative as well as positive, so although it satisﬁes a summation constraint, the
corresponding predictions are not necessarily convex combinations of the training
set target variables.
Finally, we note that the equivalent kernel (3.62) satisﬁes an important property
shared by kernel functions in general, namely that it can be expressed in the form anChapter 6
inner product with respect to a vector ψ(x) of nonlinear functions, so that
k(x,z)=ψ (x)Tψ(z) (3.65)
where ψ(x)= β1/2S1/2
N φ(x).
3.4. Bayesian Model Comparison
In Chapter 1, we highlighted the problem of over-ﬁtting as well as the use of cross-
validation as a technique for setting the values of regularization parameters or for
choosing between alternative models. Here we consider the problem of model se-
lection from a Bayesian perspective. In this section, our discussion will be very
general, and then in Section 3.5 we shall see how these ideas can be applied to the
determination of regularization parameters in linear regression.
As we shall see, the over-ﬁtting associated with maximum likelihood can be
avoided by marginalizing (summing or integrating) over the model parameters in-
stead of making point estimates of their values. Models can then be compared di-
rectly on the training data, without the need for a validation set. This allows all
available data to be used for training and avoids the multiple training runs for each
model associated with cross-validation. It also allows multiple complexity parame-
ters to be determined simultaneously as part of the training process. For example,
in Chapter 7 we shall introduce the relevance vector machine , which is a Bayesian
model having one complexity parameter for every training data point.
The Bayesian view of model comparison simply involves the use of probabilities
to represent uncertainty in the choice of model, along with a consistent application
of the sum and product rules of probability. Suppose we wish to compare a set of L
models {M
i} where i =1 ,...,L . Here a model refers to a probability distribution
over the observed data D. In the case of the polynomial curve-ﬁtting problem, the
distribution is deﬁned over the set of target values t, while the set of input values X
is assumed to be known. Other types of model deﬁne a joint distributions over X
and t. We shall suppose that the data is generated from one of these models but weSection 1.5.4
are uncertain which one. Our uncertainty is expressed through a prior probability
distribution p(Mi). Given a training set D, we then wish to evaluate the posterior
distribution
p(Mi|D) ∝ p(Mi)p(D|Mi). (3.66)
The prior allows us to express a preference for different models. Let us simply
assume that all models are given equal prior probability. The interesting term is
the model evidence p(D|Mi) which expresses the preference shown by the data for


## PDF Page 181

162 3. LINEAR MODELS FOR REGRESSION
different models, and we shall examine this term in more detail shortly. The model
evidence is sometimes also called the marginal likelihood because it can be viewed
as a likelihood function over the space of models, in which the parameters have been
marginalized out. The ratio of model evidencesp(D|Mi)/p(D|Mj) for two models
is known as a Bayes factor (Kass and Raftery, 1995).
Once we know the posterior distribution over models, the predictive distribution
is given, from the sum and product rules, by
p(t|x, D)=
L∑
i=1
p(t|x, Mi, D)p(Mi|D). (3.67)
This is an example of a mixture distribution in which the overall predictive distribu-
tion is obtained by averaging the predictive distributionsp(t|x, Mi, D) of individual
models, weighted by the posterior probabilities p(Mi|D) of those models. For in-
stance, if we have two models that are a-posteriori equally likely and one predicts
a narrow distribution around t = a while the other predicts a narrow distribution
around t = b, the overall predictive distribution will be a bimodal distribution with
modes at t = a and t = b, not a single model at t =( a + b)/2.
A simple approximation to model averaging is to use the single most probable
model alone to make predictions. This is known as model selection.
For a model governed by a set of parameters w, the model evidence is given,
from the sum and product rules of probability, by
p(D|Mi)=
∫
p(D|w, Mi)p(w|Mi)dw. (3.68)
From a sampling perspective, the marginal likelihood can be viewed as the proba-Chapter 11
bility of generating the data set D from a model whose parameters are sampled at
random from the prior. It is also interesting to note that the evidence is precisely the
normalizing term that appears in the denominator in Bayes’ theorem when evaluating
the posterior distribution over parameters because
p(w|D, M
i)= p(D|w, Mi)p(w|Mi)
p(D|Mi) . (3.69)
We can obtain some insight into the model evidence by making a simple approx-
imation to the integral over parameters. Consider ﬁrst the case of a model having a
single parameter w. The posterior distribution over parameters is proportional to
p(D|w)p(w), where we omit the dependence on the model M
i to keep the notation
uncluttered. If we assume that the posterior distribution is sharply peaked around the
most probable valuew
MAP, with width ∆ wposterior, then we can approximate the in-
tegral by the value of the integrand at its maximum times the width of the peak. If we
further assume that the prior is ﬂat with width ∆ wprior so that p(w)=1 /∆ wprior,
then we have
p(D)=
∫
p(D|w)p(w)d w ≃ p(D|wMAP)∆ wposterior
∆ wprior
(3.70)


## PDF Page 182

3.4. Bayesian Model Comparison 163
Figure 3.12 We can obtain a rough approximation to
the model evidence if we assume that
the posterior distribution over parame-
ters is sharply peaked around its mode
w
MAP.
∆wposterior
∆wprior
wMAP w
and so taking logs we obtain
lnp(D) ≃ ln p(D|wMAP)+l n
(∆ wposterior
∆ wprior
)
. (3.71)
This approximation is illustrated in Figure 3.12. The ﬁrst term represents the ﬁt to
the data given by the most probable parameter values, and for a ﬂat prior this would
correspond to the log likelihood. The second term penalizes the model according to
its complexity. Because ∆ w
posterior < ∆ wprior this term is negative, and it increases
in magnitude as the ratio ∆ wposterior/∆ wprior gets smaller. Thus, if parameters are
ﬁnely tuned to the data in the posterior distribution, then the penalty term is large.
For a model having a set ofM parameters, we can make a similar approximation
for each parameter in turn. Assuming that all parameters have the same ratio of
∆ w
posterior/∆ wprior, we obtain
lnp(D) ≃ lnp(D|wMAP)+M ln
(∆ wposterior
∆ wprior
)
. (3.72)
Thus, in this very simple approximation, the size of the complexity penalty increases
linearly with the number M of adaptive parameters in the model. As we increase
the complexity of the model, the ﬁrst term will typically decrease, because a more
complex model is better able to ﬁt the data, whereas the second term will increase
due to the dependence on M. The optimal model complexity, as determined by
the maximum evidence, will be given by a trade-off between these two competing
terms. We shall later develop a more reﬁned version of this approximation, based on
a Gaussian approximation to the posterior distribution.Section 4.4.1
We can gain further insight into Bayesian model comparison and understand
how the marginal likelihood can favour models of intermediate complexity by con-
sidering Figure 3.13. Here the horizontal axis is a one-dimensional representation
of the space of possible data sets, so that each point on this axis corresponds to a
speciﬁc data set. We now consider three models M
1, M2 and M3 of successively
increasing complexity. Imagine running these models generatively to produce exam-
ple data sets, and then looking at the distribution of data sets that result. Any given


## PDF Page 183

164 3. LINEAR MODELS FOR REGRESSION
Figure 3.13 Schematic illustration of the
distribution of data sets for
three models of different com-
plexity, in which M1 is the
simplest and M3 is the most
complex. Note that the dis-
tributions are normalized. In
this example, for the partic-
ular observed data set D
0,
the model M2 with intermedi-
ate complexity has the largest
evidence.
p(D)
DD0
M1
M2
M3
model can generate a variety of different data sets since the parameters are governed
by a prior probability distribution, and for any choice of the parameters there may
be random noise on the target variables. To generate a particular data set from a spe-
ciﬁc model, we ﬁrst choose the values of the parameters from their prior distribution
p(w), and then for these parameter values we sample the data fromp(D|w). A sim-
ple model (for example, based on a ﬁrst order polynomial) has little variability and
so will generate data sets that are fairly similar to each other. Its distribution p(D)
is therefore conﬁned to a relatively small region of the horizontal axis. By contrast,
a complex model (such as a ninth order polynomial) can generate a great variety of
different data sets, and so its distribution p(D) is spread over a large region of the
space of data sets. Because the distributions p(D|M
i) are normalized, we see that
the particular data set D0 can have the highest value of the evidence for the model
of intermediate complexity. Essentially, the simpler model cannot ﬁt the data well,
whereas the more complex model spreads its predictive probability over too broad a
range of data sets and so assigns relatively small probability to any one of them.
Implicit in the Bayesian model comparison framework is the assumption that
the true distribution from which the data are generated is contained within the set of
models under consideration. Provided this is so, we can show that Bayesian model
comparison will on average favour the correct model. To see this, consider two
models M
1 and M2 in which the truth corresponds to M1. For a given ﬁnite data
set, it is possible for the Bayes factor to be larger for the incorrect model. However, if
we average the Bayes factor over the distribution of data sets, we obtain the expected
Bayes factor in the form
∫
p(D|M1)l np(D|M1)
p(D|M2) dD (3.73)
where the average has been taken with respect to the true distribution of the data.
This quantity is an example of theKullback-Leibler divergence and satisﬁes the prop-Section 1.6.1
erty of always being positive unless the two distributions are equal in which case it
is zero. Thus on average the Bayes factor will always favour the correct model.
We have seen that the Bayesian framework avoids the problem of over-ﬁtting
and allows models to be compared on the basis of the training data alone. However,


## PDF Page 184

3.5. The Evidence Approximation 165
a Bayesian approach, like any approach to pattern recognition, needs to make as-
sumptions about the form of the model, and if these are invalid then the results can
be misleading. In particular, we see from Figure 3.12 that the model evidence can
be sensitive to many aspects of the prior, such as the behaviour in the tails. Indeed,
the evidence is not deﬁned if the prior is improper, as can be seen by noting that
an improper prior has an arbitrary scaling factor (in other words, the normalization
coefﬁcient is not deﬁned because the distribution cannot be normalized). If we con-
sider a proper prior and then take a suitable limit in order to obtain an improper prior
(for example, a Gaussian prior in which we take the limit of inﬁnite variance) then
the evidence will go to zero, as can be seen from (3.70) and Figure 3.12. It may,
however, be possible to consider the evidence ratio between two models ﬁrst and
then take a limit to obtain a meaningful answer.
In a practical application, therefore, it will be wise to keep aside an independent
test set of data on which to evaluate the overall performance of the ﬁnal system.
3.5. The Evidence Approximation
In a fully Bayesian treatment of the linear basis function model, we would intro-
duce prior distributions over the hyperparameters α and β and make predictions by
marginalizing with respect to these hyperparameters as well as with respect to the
parameters w. However, although we can integrate analytically over either w or
over the hyperparameters, the complete marginalization over all of these variables
is analytically intractable. Here we discuss an approximation in which we set the
hyperparameters to speciﬁc values determined by maximizing the marginal likeli-
hood function obtained by ﬁrst integrating over the parameters w. This framework
is known in the statistics literature as empirical Bayes (Bernardo and Smith, 1994;
Gelman et al., 2004), or type 2 maximum likelihood (Berger, 1985), or generalized
maximum likelihood (Wahba, 1975), and in the machine learning literature is also
called the evidence approximation (Gull, 1989; MacKay, 1992a).
If we introduce hyperpriors over α and β, the predictive distribution is obtained
by marginalizing over w, α and β so that
p(t|t)=
∫∫∫
p(t|w,β)p(w|t,α ,β)p(α, β|t)dw dαdβ (3.74)
where p(t|w,β) is given by (3.8) and p(w|t,α ,β) is given by (3.49) with mN and
SN deﬁned by (3.53) and (3.54) respectively. Here we have omitted the dependence
on the input variable x to keep the notation uncluttered. If the posterior distribution
p(α, β|t) is sharply peaked around values ˆα and ˆβ, then the predictive distribution is
obtained simply by marginalizing overw in which α and β are ﬁxed to the values ˆα
and ˆβ, so that
p(t|t) ≃ p(t|t, ˆα, ˆβ)=
∫
p(t|w, ˆβ)p(w|t, ˆα, ˆβ)dw. (3.75)


## PDF Page 185

166 3. LINEAR MODELS FOR REGRESSION
From Bayes’ theorem, the posterior distribution for α and β is given by
p(α, β|t) ∝ p(t|α, β)p(α, β). (3.76)
If the prior is relatively ﬂat, then in the evidence framework the values of ˆα and
ˆβ are obtained by maximizing the marginal likelihood function p(t|α, β). We shall
proceed by evaluating the marginal likelihood for the linear basis function model and
then ﬁnding its maxima. This will allow us to determine values for these hyperpa-
rameters from the training data alone, without recourse to cross-validation. Recall
that the ratio α/β is analogous to a regularization parameter.
As an aside it is worth noting that, if we deﬁne conjugate (Gamma) prior distri-
butions over α and β, then the marginalization over these hyperparameters in (3.74)
can be performed analytically to give a Student’s t-distribution over w (see Sec-
tion 2.3.7). Although the resulting integral overw is no longer analytically tractable,
it might be thought that approximating this integral, for example using the Laplace
approximation discussed (Section 4.4) which is based on a local Gaussian approxi-
mation centred on the mode of the posterior distribution, might provide a practical
alternative to the evidence framework (Buntine and Weigend, 1991). However, the
integrand as a function ofw typically has a strongly skewed mode so that the Laplace
approximation fails to capture the bulk of the probability mass, leading to poorer re-
sults than those obtained by maximizing the evidence (MacKay, 1999).
Returning to the evidence framework, we note that there are two approaches that
we can take to the maximization of the log evidence. We can evaluate the evidence
function analytically and then set its derivative equal to zero to obtain re-estimation
equations for α and β, which we shall do in Section 3.5.2. Alternatively we use a
technique called the expectation maximization (EM) algorithm, which will be dis-
cussed in Section 9.3.4 where we shall also show that these two approaches converge
to the same solution.
3.5.1 Evaluation of the evidence function
The marginal likelihood function p(t|α, β) is obtained by integrating over the
weight parameters w, so that
p(t|α, β)=
∫
p(t|w,β)p(w|α)dw. (3.77)
One way to evaluate this integral is to make use once again of the result (2.115)
for the conditional distribution in a linear-Gaussian model. Here we shall evaluateExercise 3.16
the integral instead by completing the square in the exponent and making use of the
standard form for the normalization coefﬁcient of a Gaussian.
From (3.11), (3.12), and (3.52), we can write the evidence function in the formExercise 3.17
p(t|α, β)=
( β
2π
)N/2 (α
2π
)M/2 ∫
exp {−E(w)} dw (3.78)


## PDF Page 186

3.5. The Evidence Approximation 167
where M is the dimensionality of w, and we have deﬁned
E(w)=βE D(w)+ αEW (w)
= β
2 ∥t − Φw∥2 + α
2wTw. (3.79)
We recognize (3.79) as being equal, up to a constant of proportionality, to the reg-
ularized sum-of-squares error function (3.27). We now complete the square over wExercise 3.18
giving
E(w)=E (mN )+ 1
2(w − mN )TA(w − mN ) (3.80)
where we have introduced
A = αI + βΦTΦ (3.81)
together with
E(mN )= β
2 ∥t − ΦmN ∥2 + α
2mT
NmN . (3.82)
Note that A corresponds to the matrix of second derivatives of the error function
A = ∇∇ E(w) (3.83)
and is known as the Hessian matrix. Here we have also deﬁned mN given by
mN = βA−1ΦTt. (3.84)
Using (3.54), we see that A = S−1
N , and hence (3.84) is equivalent to the previous
deﬁnition (3.53), and therefore represents the mean of the posterior distribution.
The integral over w can now be evaluated simply by appealing to the standard
result for the normalization coefﬁcient of a multivariate Gaussian, givingExercise 3.19
∫
exp {−E(w)} dw
=e x p {−E(mN )}
∫
exp
{
− 1
2(w − mN )TA(w − mN )
}
dw
=e x p {−E(mN )}(2π)M/2|A|−1/2. (3.85)
Using (3.78) we can then write the log of the marginal likelihood in the form
lnp(t|α, β)= M
2 ln α + N
2 lnβ − E(mN ) − 1
2 ln |A|− N
2 ln(2π) (3.86)
which is the required expression for the evidence function.
Returning to the polynomial regression problem, we can plot the model evidence
against the order of the polynomial, as shown in Figure 3.14. Here we have assumed
a prior of the form (1.65) with the parameter α ﬁxed at α =5 × 10−3. The form
of this plot is very instructive. Referring back to Figure 1.4, we see that the M =0
polynomial has very poor ﬁt to the data and consequently gives a relatively low value


## PDF Page 187

168 3. LINEAR MODELS FOR REGRESSION
Figure 3.14 Plot of the model evidence versus
the order M, for the polynomial re-
gression model, showing that the
evidence favours the model with
M =3 .
M
0 2 4 6 8
−26
−24
−22
−20
−18
for the evidence. Going to the M =1 polynomial greatly improves the data ﬁt, and
hence the evidence is signiﬁcantly higher. However, in going to M =2 , the data
ﬁt is improved only very marginally, due to the fact that the underlying sinusoidal
function from which the data is generated is an odd function and so has no even terms
in a polynomial expansion. Indeed, Figure 1.5 shows that the residual data error is
reduced only slightly in going from M =1 to M =2 . Because this richer model
suffers a greater complexity penalty, the evidence actually falls in going fromM =1
to M =2 . When we go to M =3 we obtain a signiﬁcant further improvement in
data ﬁt, as seen in Figure 1.4, and so the evidence is increased again, giving the
highest overall evidence for any of the polynomials. Further increases in the value
of M produce only small improvements in the ﬁt to the data but suffer increasing
complexity penalty, leading overall to a decrease in the evidence values. Looking
again at Figure 1.5, we see that the generalization error is roughly constant between
M =3 and M =8 , and it would be difﬁcult to choose between these models on
the basis of this plot alone. The evidence values, however, show a clear preference
for M =3 , since this is the simplest model which gives a good explanation for the
observed data.
3.5.2 Maximizing the evidence function
Let us ﬁrst consider the maximization of p(t|α, β) with respect to α. This can
be done by ﬁrst deﬁning the following eigenvector equation
(
βΦTΦ
)
ui = λiui. (3.87)
From (3.81), it then follows thatA has eigenvaluesα+λi. Now consider the deriva-
tive of the term involvingln |A| in (3.86) with respect to α.W eh a v e
d
dα ln |A| = d
dα ln
∏
i
(λi + α)= d
dα
∑
i
ln(λi + α)=
∑
i
1
λi + α. (3.88)
Thus the stationary points of (3.86) with respect to α satisfy
0= M
2α − 1
2mT
NmN − 1
2
∑
i
1
λi + α. (3.89)


## PDF Page 188

3.5. The Evidence Approximation 169
Multiplying through by 2α and rearranging, we obtain
αmT
NmN = M − α
∑
i
1
λi + α = γ. (3.90)
Since there are M terms in the sum over i, the quantity γ can be written
γ =
∑
i
λi
α + λi
. (3.91)
The interpretation of the quantity γ will be discussed shortly. From (3.90) we see
that the value of α that maximizes the marginal likelihood satisﬁesExercise 3.20
α = γ
mT
NmN
. (3.92)
Note that this is an implicit solution for α not only because γ depends on α, but also
because the mode mN of the posterior distribution itself depends on the choice of
α. We therefore adopt an iterative procedure in which we make an initial choice for
α and use this to ﬁnd mN , which is given by (3.53), and also to evaluate γ, which
is given by (3.91). These values are then used to re-estimate α using (3.92), and the
process repeated until convergence. Note that because the matrix ΦTΦ is ﬁxed, we
can compute its eigenvalues once at the start and then simply multiply these by β to
obtain the λi.
It should be emphasized that the value ofα has been determined purely by look-
ing at the training data. In contrast to maximum likelihood methods, no independent
data set is required in order to optimize the model complexity.
We can similarly maximize the log marginal likelihood (3.86) with respect toβ.
To do this, we note that the eigenvalues λi deﬁned by (3.87) are proportional to β,
and hence dλi/dβ = λi/β giving
d
dβ ln |A| = d
dβ
∑
i
ln(λi + α)= 1
β
∑
i
λi
λi + α = γ
β. (3.93)
The stationary point of the marginal likelihood therefore satisﬁes
0= N
2β − 1
2
N∑
n=1
{
tn − mT
N φ(xn)
}2
− γ
2β (3.94)
and rearranging we obtainExercise 3.22
1
β = 1
N − γ
N∑
n=1
{
tn − mT
N φ(xn)
}2
. (3.95)
Again, this is an implicit solution for β and can be solved by choosing an initial
value for β and then using this to calculate mN and γ and then re-estimate β using
(3.95), repeating until convergence. If both α and β are to be determined from the
data, then their values can be re-estimated together after each update of γ.


## PDF Page 189

170 3. LINEAR MODELS FOR REGRESSION
Figure 3.15 Contours of the likelihood function (red)
and the prior (green) in which the axes in parameter
space have been rotated to align with the eigenvectors
ui of the Hessian. For α =0 , the mode of the poste-
rior is given by the maximum likelihood solution wML,
whereas for nonzero α the mode is at wMAP = mN .I n
the direction w1 the eigenvalue λ1, deﬁned by (3.87), is
small compared with α and so the quantity λ1/(λ1 + α)
is close to zero, and the corresponding MAP value of
w
1 is also close to zero. By contrast, in the direction w2
the eigenvalue λ2 is large compared with α and so the
quantity λ2/(λ2 +α) is close to unity, and the MAP value
of w2 is close to its maximum likelihood value.
u1
u2
w1
w2
wMAP
wML
3.5.3 Effective number of parameters
The result (3.92) has an elegant interpretation (MacKay, 1992a), which provides
insight into the Bayesian solution forα. To see this, consider the contours of the like-
lihood function and the prior as illustrated in Figure 3.15. Here we have implicitly
transformed to a rotated set of axes in parameter space aligned with the eigenvec-
tors ui deﬁned in (3.87). Contours of the likelihood function are then axis-aligned
ellipses. The eigenvalues λi measure the curvature of the likelihood function, and
so in Figure 3.15 the eigenvalue λ1 is small compared with λ2 (because a smaller
curvature corresponds to a greater elongation of the contours of the likelihood func-
tion). Because βΦTΦ is a positive deﬁnite matrix, it will have positive eigenvalues,
and so the ratio λi/(λi + α) will lie between 0 and 1. Consequently, the quantity γ
deﬁned by (3.91) will lie in the range 0 ⩽ γ ⩽ M. For directions in which λi ≫ α,
the corresponding parameter wi will be close to its maximum likelihood value, and
the ratio λi/(λi + α) will be close to 1. Such parameters are called well determined
because their values are tightly constrained by the data. Conversely, for directions
in which λ
i ≪ α, the corresponding parameters wi will be close to zero, as will the
ratios λi/(λi +α). These are directions in which the likelihood function is relatively
insensitive to the parameter value and so the parameter has been set to a small value
by the prior. The quantity γ deﬁned by (3.91) therefore measures the effective total
number of well determined parameters.
We can obtain some insight into the result (3.95) for re-estimating β by com-
paring it with the corresponding maximum likelihood result given by (3.21). Both
of these formulae express the variance (the inverse precision) as an average of the
squared differences between the targets and the model predictions. However, they
differ in that the number of data points N in the denominator of the maximum like-
lihood result is replaced by N − γ in the Bayesian result. We recall from (1.56) that
the maximum likelihood estimate of the variance for a Gaussian distribution over a


## PDF Page 190

3.5. The Evidence Approximation 171
single variable x is given by
σ2
ML = 1
N
N∑
n=1
(xn − µML)2 (3.96)
and that this estimate is biased because the maximum likelihood solution µML for
the mean has ﬁtted some of the noise on the data. In effect, this has used up one
degree of freedom in the model. The corresponding unbiased estimate is given by
(1.59) and takes the form
σ2
MAP = 1
N − 1
N∑
n=1
(xn − µML)2. (3.97)
We shall see in Section 10.1.3 that this result can be obtained from a Bayesian treat-
ment in which we marginalize over the unknown mean. The factor of N − 1 in the
denominator of the Bayesian result takes account of the fact that one degree of free-
dom has been used in ﬁtting the mean and removes the bias of maximum likelihood.
Now consider the corresponding results for the linear regression model. The mean
of the target distribution is now given by the function w
Tφ(x), which contains M
parameters. However, not all of these parameters are tuned to the data. The effective
number of parameters that are determined by the data isγ, with the remainingM −γ
parameters set to small values by the prior. This is reﬂected in the Bayesian result
for the variance that has a factor N − γ in the denominator, thereby correcting for
the bias of the maximum likelihood result.
We can illustrate the evidence framework for setting hyperparameters using the
sinusoidal synthetic data set from Section 1.1, together with the Gaussian basis func-
tion model comprising 9 basis functions, so that the total number of parameters in
the model is given by M =1 0 including the bias. Here, for simplicity of illustra-
tion, we have set β to its true value of 11.1 and then used the evidence framework to
determine α, as shown in Figure 3.16.
We can also see how the parameter α controls the magnitude of the parameters
{wi}, by plotting the individual parameters versus the effective numberγ of param-
eters, as shown in Figure 3.17.
If we consider the limit N ≫ M in which the number of data points is large in
relation to the number of parameters, then from (3.87) all of the parameters will be
well determined by the data becauseΦTΦ involves an implicit sum over data points,
and so the eigenvalues λi increase with the size of the data set. In this case, γ = M,
and the re-estimation equations for α and β become
α = M
2EW (mN ) (3.98)
β = N
2ED(mN ) (3.99)
where EW and ED are deﬁned by (3.25) and (3.26), respectively. These results
can be used as an easy-to-compute approximation to the full evidence re-estimation


## PDF Page 191

172 3. LINEAR MODELS FOR REGRESSION
lnα
−5 0 5
lnα
−5 0 5
Figure 3.16 The left plot shows γ (red curve) and 2αEW (mN ) (blue curve) versus ln α for the sinusoidal
synthetic data set. It is the intersection of these two curves that deﬁnes the optimum value for α given by the
evidence procedure. The right plot shows the corresponding graph of log evidence ln p(t|α, β) versus ln α (red
curve) showing that the peak coincides with the crossing point of the curves in the left plot. Also shown is the
test set error (blue curve) showing that the evidence maximum occurs close to the point of best generalization.
formulae, because they do not require evaluation of the eigenvalue spectrum of the
Hessian.
Figure 3.17 Plot of the 10 parameters wi
from the Gaussian basis function
model versus the effective num-
ber of parameters γ, in which the
hyperparameter α is varied in the
range 0 ⩽ α ⩽ ∞ causing γ to
vary in the range 0 ⩽ γ ⩽ M.
9
7
1
3
6
2
5
4
8
0
γ
wi
0 2 4 6 8 10
−2
−1
0
1
2
3.6. Limitations of Fixed Basis Functions
Throughout this chapter, we have focussed on models comprising a linear combina-
tion of ﬁxed, nonlinear basis functions. We have seen that the assumption of linearity
in the parameters led to a range of useful properties including closed-form solutions
to the least-squares problem, as well as a tractable Bayesian treatment. Furthermore,
for a suitable choice of basis functions, we can model arbitrary nonlinearities in the


## PDF Page 192

Exercises 173
mapping from input variables to targets. In the next chapter, we shall study an anal-
ogous class of models for classiﬁcation.
It might appear, therefore, that such linear models constitute a general purpose
framework for solving problems in pattern recognition. Unfortunately, there are
some signiﬁcant shortcomings with linear models, which will cause us to turn in
later chapters to more complex models such as support vector machines and neural
networks.
The difﬁculty stems from the assumption that the basis functions φ
j(x) are ﬁxed
before the training data set is observed and is a manifestation of the curse of dimen-
sionality discussed in Section 1.4. As a consequence, the number of basis functions
needs to grow rapidly, often exponentially, with the dimensionality D of the input
space.
Fortunately, there are two properties of real data sets that we can exploit to help
alleviate this problem. First of all, the data vectors {x
n} typically lie close to a non-
linear manifold whose intrinsic dimensionality is smaller than that of the input space
as a result of strong correlations between the input variables. We will see an example
of this when we consider images of handwritten digits in Chapter 12. If we are using
localized basis functions, we can arrange that they are scattered in input space only
in regions containing data. This approach is used in radial basis function networks
and also in support vector and relevance vector machines. Neural network models,
which use adaptive basis functions having sigmoidal nonlinearities, can adapt the
parameters so that the regions of input space over which the basis functions vary
corresponds to the data manifold. The second property is that target variables may
have signiﬁcant dependence on only a small number of possible directions within the
data manifold. Neural networks can exploit this property by choosing the directions
in input space to which the basis functions respond.
Exercises
3.1 (⋆) www Show that the ‘tanh’ function and the logistic sigmoid function (3.6)
are related by
tanh(a)=2 σ(2a) − 1. (3.100)
Hence show that a general linear combination of logistic sigmoid functions of the
form
y(x,w)=w
0 +
M∑
j=1
wjσ
(x − µj
s
)
(3.101)
is equivalent to a linear combination of ‘tanh’ functions of the form
y(x,u)= u0 +
M∑
j=1
uj tanh
(x − µj
s
)
(3.102)
and ﬁnd expressions to relate the new parameters {u1,...,u M } to the original pa-
rameters {w1,...,w M }.


## PDF Page 193

174 3. LINEAR MODELS FOR REGRESSION
3.2 (⋆⋆ ) Show that the matrix
Φ(ΦTΦ)−1ΦT (3.103)
takes any vector v and projects it onto the space spanned by the columns of Φ. Use
this result to show that the least-squares solution (3.15) corresponds to an orthogonal
projection of the vector t onto the manifold S as shown in Figure 3.2.
3.3 (⋆) Consider a data set in which each data point tn is associated with a weighting
factor rn > 0, so that the sum-of-squares error function becomes
ED(w)= 1
2
N∑
n=1
rn
{
tn − wTφ(xn)
}2
. (3.104)
Find an expression for the solution w⋆ that minimizes this error function. Give two
alternative interpretations of the weighted sum-of-squares error function in terms of
(i) data dependent noise variance and (ii) replicated data points.
3.4 (⋆) www Consider a linear model of the form
y(x,w)=w 0 +
D∑
i=1
wixi (3.105)
together with a sum-of-squares error function of the form
ED(w)= 1
2
N∑
n=1
{y(xn,w) − tn}2 . (3.106)
Now suppose that Gaussian noise ϵi with zero mean and variance σ2 is added in-
dependently to each of the input variables xi. By making use of E[ϵi]=0 and
E[ϵiϵj]= δijσ2, show that minimizing ED averaged over the noise distribution is
equivalent to minimizing the sum-of-squares error for noise-free input variables with
the addition of a weight-decay regularization term, in which the bias parameter w0
is omitted from the regularizer.
3.5 (⋆) www Using the technique of Lagrange multipliers, discussed in Appendix E,
show that minimization of the regularized error function (3.29) is equivalent to mini-
mizing the unregularized sum-of-squares error (3.12) subject to the constraint (3.30).
Discuss the relationship between the parameters ηand λ.
3.6 (⋆)
www Consider a linear basis function regression model for a multivariate
target variable t having a Gaussian distribution of the form
p(t|W,Σ)=N (t|y(x,W),Σ) (3.107)
where
y(x,W)=W Tφ(x) (3.108)


## PDF Page 194

Exercises 175
together with a training data set comprising input basis vectors φ(xn) and corre-
sponding target vectors tn, with n =1 ,...,N . Show that the maximum likelihood
solution WML for the parameter matrix W has the property that each column is
given by an expression of the form (3.15), which was the solution for an isotropic
noise distribution. Note that this is independent of the covariance matrix Σ. Show
that the maximum likelihood solution for Σ is given by
Σ = 1
N
N∑
n=1
(
tn − WT
MLφ(xn)
)(
tn − WT
MLφ(xn)
)T
. (3.109)
3.7 (⋆) By using the technique of completing the square, verify the result (3.49) for the
posterior distribution of the parametersw in the linear basis function model in which
mN and SN are deﬁned by (3.50) and (3.51) respectively.
3.8 (⋆⋆ ) www Consider the linear basis function model in Section 3.1, and suppose
that we have already observed N data points, so that the posterior distribution over
w is given by (3.49). This posterior can be regarded as the prior for the next obser-
vation. By considering an additional data point (xN+1,t N+1), and by completing
the square in the exponential, show that the resulting posterior distribution is again
given by (3.49) but withSN replaced by SN+1 and mN replaced by mN+1.
3.9 (⋆⋆ ) Repeat the previous exercise but instead of completing the square by hand,
make use of the general result for linear-Gaussian models given by (2.116).
3.10 (⋆⋆ ) www By making use of the result (2.115) to evaluate the integral in (3.57),
verify that the predictive distribution for the Bayesian linear regression model is
given by (3.58) in which the input-dependent variance is given by (3.59).
3.11 (⋆⋆ ) We have seen that, as the size of a data set increases, the uncertainty associated
with the posterior distribution over model parameters decreases. Make use of the
matrix identity (Appendix C)
(
M + vvT)−1
= M−1 − (M−1v)
(
vTM−1)
1+v TM−1v (3.110)
to show that the uncertainty σ2
N (x) associated with the linear regression function
given by (3.59) satisﬁes
σ2
N+1(x) ⩽ σ2
N (x). (3.111)
3.12 (⋆⋆ ) We saw in Section 2.3.6 that the conjugate prior for a Gaussian distribution
with unknown mean and unknown precision (inverse variance) is a normal-gamma
distribution. This property also holds for the case of the conditional Gaussian dis-
tribution p(t|x,w,β) of the linear regression model. If we consider the likelihood
function (3.10), then the conjugate prior for w and β is given by
p(w,β)=N (w|m
0,β −1S0)Gam(β|a0,b0). (3.112)


## PDF Page 195

176 3. LINEAR MODELS FOR REGRESSION
Show that the corresponding posterior distribution takes the same functional form,
so that
p(w,β |t)=N (w|mN ,β −1SN )Gam(β|aN ,b N ) (3.113)
and ﬁnd expressions for the posterior parameters mN , SN , aN , and bN .
3.13 (⋆⋆ ) Show that the predictive distribution p(t|x, t) for the model discussed in Ex-
ercise 3.12 is given by a Student’s t-distribution of the form
p(t|x, t)=S t (t|µ, λ, ν) (3.114)
and obtain expressions for µ, λ and ν.
3.14 (⋆⋆ ) In this exercise, we explore in more detail the properties of the equivalent
kernel deﬁned by (3.62), where SN is deﬁned by (3.54). Suppose that the basis
functions φj(x) are linearly independent and that the number N of data points is
greater than the number M of basis functions. Furthermore, let one of the basis
functions be constant, say φ0(x)=1 . By taking suitable linear combinations of
these basis functions, we can construct a new basis set ψj(x) spanning the same
space but that are orthonormal, so that
N∑
n=1
ψj(xn)ψk(xn)=I jk (3.115)
where Ijk is deﬁned to be 1 if j = k and 0 otherwise, and we take ψ0(x)=1 . Show
that for α =0 , the equivalent kernel can be written as k(x,x′)= ψ(x)Tψ(x′)
where ψ =( ψ1,...,ψ M )T. Use this result to show that the kernel satisﬁes the
summation constraint
N∑
n=1
k(x,xn)=1 . (3.116)
3.15 (⋆) www Consider a linear basis function model for regression in which the pa-
rameters α and β are set using the evidence framework. Show that the function
E(mN ) deﬁned by (3.82) satisﬁes the relation 2E(mN )=N .
3.16 (⋆⋆ ) Derive the result (3.86) for the log evidence function p(t|α, β) of the linear
regression model by making use of (2.115) to evaluate the integral (3.77) directly.
3.17 (⋆) Show that the evidence function for the Bayesian linear regression model can
be written in the form (3.78) in which E(w) is deﬁned by (3.79).
3.18 (⋆⋆ ) www By completing the square over w, show that the error function (3.79)
in Bayesian linear regression can be written in the form (3.80).
3.19 (⋆⋆ ) Show that the integration overw in the Bayesian linear regression model gives
the result (3.85). Hence show that the log marginal likelihood is given by (3.86).


## PDF Page 196

Exercises 177
3.20 (⋆⋆ ) www Starting from (3.86) verify all of the steps needed to show that maxi-
mization of the log marginal likelihood function (3.86) with respect toα leads to the
re-estimation equation (3.92).
3.21 (⋆⋆ ) An alternative way to derive the result (3.92) for the optimal value ofα in the
evidence framework is to make use of the identity
d
dα ln |A| = Tr
(
A−1 d
dαA
)
. (3.117)
Prove this identity by considering the eigenvalue expansion of a real, symmetric
matrix A, and making use of the standard results for the determinant and trace of
A expressed in terms of its eigenvalues (Appendix C). Then make use of (3.117) to
derive (3.92) starting from (3.86).
3.22 (⋆⋆ ) Starting from (3.86) verify all of the steps needed to show that maximiza-
tion of the log marginal likelihood function (3.86) with respect to β leads to the
re-estimation equation (3.95).
3.23 (⋆⋆ ) www Show that the marginal probability of the data, in other words the
model evidence, for the model described in Exercise 3.12 is given by
p(t)= 1
(2π)N/2
ba0
0
baN
N
Γ(aN )
Γ(a0)
|SN |1/2
|S0|1/2 (3.118)
by ﬁrst marginalizing with respect to w and then with respect to β.
3.24 (⋆⋆ ) Repeat the previous exercise but now use Bayes’ theorem in the form
p(t)= p(t|w,β)p(w,β)
p(w,β |t) (3.119)
and then substitute for the prior and posterior distributions and the likelihood func-
tion in order to derive the result (3.118).
