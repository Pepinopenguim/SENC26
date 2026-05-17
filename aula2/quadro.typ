#set text(18pt)

O texto *'On the Calculation of Arbitrary Moments of Polygons'* busca definir uma fórmula geral para calcular qualquer *momento* de qualquer *Polígono* conhecidos apenas os pontos que o definem.

Primeiro, vamos observar a definição abaixo

$
nu_(p, q) = ∬_R x^p y^q d x d y 
$

Ou seja, $nu$ representa o momento de order $p$ e $q$, para $x$ e $y$ para o polígono R.

Ou seja, podemos calcular a área desse polígono se $p = 0$ e $q = 0$:

$
  a = ∬_R d x d y
$

E assim, ele normaliza $nu$ definindo $alpha$:

$
    alpha_(p,q) = nu_(p,q) / a = 1/ a ∬_R x^p y^q d x d y 
$

Beleza, mas isso não é tão importante assim! Tudo que importa é entendermos as fórmulas abaixo, e como relacionar elas com os momentos de inércia:



$
  a = 1/2 sum_(i=1)^n x_(i-1)y_i - x_i y_(i-1)
$ #footnote[Conhecida como a fórmula de shoelace]

$
  alpha_(2,0) = 1/(12a) sum_(i=1)^n (x_(i-1)y_i - x_i y_(i-1))(x_(i-1)^2+x_(i-1) x_i +x_i^2)
$

$
  alpha_(0,2) = 1/(12a) sum_(i=1)^n (x_(i-1)y_i - x_i y_(i-1))(y_(i-1)^2+y_(i-1) y_i +y_i^2)
$

Lembre-se, a equação dos momentos de inércia é:

$
  I_x = ∬_R y^2 d x d y = nu_(0,2) = alpha_(0,2) dot a
$

$
  I_y = ∬_R x^2 d x d y = nu_(2, 0) = alpha_(2,0) dot a
$

Para calcular os centroides, basta conhecer os primeiros momentos

$
  x_c = Q_x / a = (∬_R x d x d y) / a = alpha_(1,0)
$

$
  y_c = Q_y / a = (∬_R y d x d y) / a = alpha_(0,1)
$


$
  x_c = alpha_(1,0) = 1/(6a) sum_(i=1)^n (x_(i-1)y_i - x_i y_(i-1))(x_(i-1) + x_i)
$

$
  y_c = alpha_(0,1) = 1/(6a) sum_(i=1)^n (x_(i-1)y_i - x_i y_(i-1))(y_(i-1) + y_i)
$

Para determinar o momento de inércia em torno do centróide, basta conhecer área e o centróide, pelo teorema dos eixos paralelos:

$
  I_x = I_(x_c) + A dot y_c ^2
$

$
  I_(x_c) = I_x - A dot y_c ^2
$

E vice-e-versa para $I_y$.
