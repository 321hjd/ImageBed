% 功能：比较最速下降、牛顿法和共轭梯度法搜索最优解的过程
% author：hjd
% last-modified：2022/5/13

clear
syms x1 x2 
f = @(x1,x2) x1.^2 + x1.*x2 + 3*x2.^2;       % 只需要修改此处的函数表达时即可 
% f = @(x1,x2) (x1+x2).^2 + (x1+1).^2 + (x2+3).^2;
eps = 1e-5;
[X1,X2] = meshgrid(-2:0.1:2);
Y = f(X1,X2);
contour(X1,X2,Y);

%% 最速下降法
% 最速下降法搜索最优解的过程是锯齿形的，尤其是在接近最优解的迭代点时
% 因为该算法只能保证在每次迭代时朝着该点下降最快的方向迭代，而不考虑迭代后的坡度
% 与梯度下降法相比，最速下降多了一步一维搜索，找到令目标函数最小的迭代步长，梯度下降是预先设置好步长
var = [x1 x2];
x0 = [1 1];
[min_x,min_f,x_iter,y_iter,k] = steepestDescent(f,x0,var,eps); % 调整容差，可以获得更高的精度

hold on
p1 = plot(x_iter(:,1),x_iter(:,2),'-*');
hold off
xlabel('x1');ylabel('x2');

%% 牛顿法
% 牛顿法比最速下降收敛更快，因为不仅考虑了什么方向下降更快，还考虑了下降之后的坡度
% 对于二次问题，牛顿法可一步求解
var = [x1;x2];
x0 = [1;1];
[min_x,min_f,x_iter,y_iter,k] = Newton(f,x0,var,eps);

hold on
p2 = plot(x_iter(:,1),x_iter(:,2),'-o');
hold off
xlabel('x1');ylabel('x2');

%% 共轭梯度法
% 共轭梯度法介于最速下降和牛顿法之间的方法
% 只需要一阶导数信息，不用像牛顿法一样求Hessian矩阵并求逆，但克服了最速下降法收敛慢的缺点
% “步收敛性”：每一步都走到极致，即每一维都只需要搜索一次，因此N维空间只需要搜索N次即可收敛
var = [x1;x2];
x0 = [1;1];
[min_x,min_f,x_iter,y_iter,k] = conjungateGradient(f,x0,var,eps);
hold on
p3 = plot(x_iter(:,1),x_iter(:,2),'-gs');
hold off
xlabel('x1');ylabel('x2');

%% 三个算法的搜索过程放在一张图
legend([p1,p2,p3],{'steepestDescent','Newton','conjungateGradient'});