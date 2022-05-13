function [min_x,min_f,x_iter,y_iter,k] = Newton(f,x0,var,eps)
%   功能：利用牛顿法计算无约束目标函数极小值
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
    f_sym = sym(f);                             % 创建一个符号f_sym(注意：f不能接收向量)
    F_grad = matlabFunction(gradient(f_sym));   % 求梯度函数句柄
    F_hessian = matlabFunction(hessian(f_sym)); % 求hessian矩阵函数句柄
    F_grad = sym(F_grad);
    F_hessian = sym(F_hessian);
    x = x0;
    k = 1;                  % 迭代编号
    x_iter(:,k) = x;
    y_iter(k,:) = double(subs(f_sym,var,x));
    % 迭代
    while true
%         f_grad = F_grad(x0(1),x0(2));
        f_grad = double(subs(F_grad,var,x));
%         f_hessian = F_hessian(x0(1),x0(2));
        f_hessian = double(subs(F_hessian,var,x));
        if norm(f_grad) < eps
            break;
        end
        x = x - f_hessian\f_grad;               % 变量迭代
        k = k + 1;
        x_iter(:,k) = x;
        y_iter(k,:) = double(subs(f_sym,var,x));  
    end
    min_x = x;
    x_iter = x_iter';
    min_f = double(subs(f_sym,var,min_x));
    k = k - 1;
end