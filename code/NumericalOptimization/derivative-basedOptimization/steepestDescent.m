function [min_x,min_f,x_iter,y_iter,k] = steepestDescent(f,x0,var,eps)
%   功能：利用最速下降法计算无约束目标函数极小值
%   author：hjd
%   last-modified：2022/5/13
%   输入
%       f       -------     目标函数（sym）
%       x0      -------     初始点（向量）
%       var     -------     自变量（符号变量sym），如sym x1 x2, var = [x1,x2]
%       eps     -------     精度
%	输出
%       min_x   -------     最小值点
%       min_f   -------     最小值
%       x_iter  -------     每次迭代点
%       y_iter  -------     迭代值
%       k       -------     迭代次数
    syms lambdas;
    f_sym = sym(f);
    j = jacobian(f,var);    % 计算函数的雅可比矩阵（一阶导）,等价于下面两个式子
%     F_grad = matlabFunction(gradient(f_sym));   % 求梯度函数句柄
%     F_grad = sym(F_grad);
    x = x0;
    k = 1;                  % 迭代编号
    x_iter(k,:) = x;
    y_iter(k,:) = double(subs(f_sym,var,x));  
    while true
        grad = (double(subs(j,var,x)));             % 计算梯度。subs函数,将符号变量var替换为数值x
        if norm(grad,2) > eps                       % 算法终止条件
            f_a = subs(f_sym,var,x - lambdas*grad);
            f_diff = simplify(diff(f_a,lambdas));   % 对步长求导令其等于零，寻找最大步长      
            lambda = max(double(solve(f_diff)));    % 求解步长lambda
            x = double(x - lambda*grad);            % 产生新迭代点；
            k = k + 1;
            x_iter(k,:) = x;
            y_iter(k,:) = double(subs(f_sym,var,x));
        else
            break
        end
    end
    min_x = x;                                      % 最优解
    min_f = double(subs(f_sym,var,min_x));          % 目标函数最小值
    k = k - 1;
end