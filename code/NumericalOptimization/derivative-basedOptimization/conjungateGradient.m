function [min_x,min_f,x_iter,y_iter,k] = conjungateGradient(f,x0,var,eps)
%   功能：利用共轭梯度法计算无约束目标函数极小值
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
    syms lambdas
    f_sym = sym(f);                             % 创建一个符号f_sym(注意：f不能接收向量)
    F_grad = matlabFunction(gradient(f_sym));   % 求梯度函数句柄
    F_grad = sym(F_grad);                       % f的梯度（一阶导）
    k = 0;                                      % 迭代编号
    n = length(x0);                             % 变量的维数，共轭梯度法最多搜索n步即可得到最优解  
    x = x0;
    x_iter(1,:) = x0;                           % 存储初始点
    y_iter(1,:) = double(subs(f_sym,var,x));    % 初始函数值
    grad = double(subs(F_grad,var,x));          % 梯度值
    r = grad;                                   % 初始残差
    p = -r;                                     % 第一个共轭向量（下降方向）
    r_pre = r;                                  % 存储每一步的残差，用于计算共轭向量的迭代步长beta_k
    % 迭代
    while(norm(r) > eps || k < n)
        % 1.一维搜索，确定步长lambda
        % （sym）x_{k+1} = x_{k} + lambda p_k
        x = x + lambdas*p;
        f_a = subs(f_sym,var,x);
        f_diff = simplify(diff(f_a,lambdas));   % 对步长求导令其等于零，寻找最大步长      
        lambda = max(double(solve(f_diff)));    % 求解步长lambda
        % 如果lambda太小，算法终止，节省时间
        if lambda < 1e-5
            break;
        end
        
        % 2.更新
        % 更新迭代点
        % （数值）x_{k+1} = x_{k} + lambda p_k
        x = double(subs(x,lambdas,lambda));
        % 更新残差（其实就是每次迭代后对应在x_{k+1}的梯度）
        r = double(subs(F_grad,var,x));
        % 共轭向量步长beta_k的确定：beta_k=r_{k}^{T}r_{k}/r_{k-1}^{T}r_{k-1}
        beta = sumsqr(r)/sumsqr(r_pre);         % sumsqr是矩阵元素平方和
        % 下一个共轭向量
        p = -r + beta*p;
        
        k = k + 1;
        x_iter(k+1,:) = x;
        y_iter(k+1,:) = double(subs(f_sym,var,x));
    end
    
    % 输出
    min_x = x;
    min_f = double(subs(f_sym,var,x));
end

