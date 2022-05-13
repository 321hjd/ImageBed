function [min_x,min_f,x_iter,y_iter,k] = conjungateGradient(f,x0,var,eps)
%   ���ܣ����ù����ݶȷ�������Լ��Ŀ�꺯����Сֵ
%   author��hjd
%   last-modified��2022/5/13
%   ����
%       f       -------     Ŀ�꺯����sym��
%       x0      -------     ��ʼ�㣨������
%       var     -------     �Ա��������ű���sym������sym x1 x2, var = [x1,x2]
%       eps     -------     ����
%	���
%       min_x   -------     ��Сֵ��
%       min_f   -------     ��Сֵ
%       x_iter  -------     ÿ�ε�����
%       y_iter  -------     ����ֵ
%       k       -------     ��������
    syms lambdas
    f_sym = sym(f);                             % ����һ������f_sym(ע�⣺f���ܽ�������)
    F_grad = matlabFunction(gradient(f_sym));   % ���ݶȺ������
    F_grad = sym(F_grad);                       % f���ݶȣ�һ�׵���
    k = 0;                                      % �������
    n = length(x0);                             % ������ά���������ݶȷ��������n�����ɵõ����Ž�  
    x = x0;
    x_iter(1,:) = x0;                           % �洢��ʼ��
    y_iter(1,:) = double(subs(f_sym,var,x));    % ��ʼ����ֵ
    grad = double(subs(F_grad,var,x));          % �ݶ�ֵ
    r = grad;                                   % ��ʼ�в�
    p = -r;                                     % ��һ�������������½�����
    r_pre = r;                                  % �洢ÿһ���Ĳв���ڼ��㹲�������ĵ�������beta_k
    % ����
    while(norm(r) > eps || k < n)
        % 1.һά������ȷ������lambda
        % ��sym��x_{k+1} = x_{k} + lambda p_k
        x = x + lambdas*p;
        f_a = subs(f_sym,var,x);
        f_diff = simplify(diff(f_a,lambdas));   % �Բ�������������㣬Ѱ����󲽳�      
        lambda = max(double(solve(f_diff)));    % ��ⲽ��lambda
        % ���lambda̫С���㷨��ֹ����ʡʱ��
        if lambda < 1e-5
            break;
        end
        
        % 2.����
        % ���µ�����
        % ����ֵ��x_{k+1} = x_{k} + lambda p_k
        x = double(subs(x,lambdas,lambda));
        % ���²в��ʵ����ÿ�ε������Ӧ��x_{k+1}���ݶȣ�
        r = double(subs(F_grad,var,x));
        % ������������beta_k��ȷ����beta_k=r_{k}^{T}r_{k}/r_{k-1}^{T}r_{k-1}
        beta = sumsqr(r)/sumsqr(r_pre);         % sumsqr�Ǿ���Ԫ��ƽ����
        % ��һ����������
        p = -r + beta*p;
        
        k = k + 1;
        x_iter(k+1,:) = x;
        y_iter(k+1,:) = double(subs(f_sym,var,x));
    end
    
    % ���
    min_x = x;
    min_f = double(subs(f_sym,var,x));
end

