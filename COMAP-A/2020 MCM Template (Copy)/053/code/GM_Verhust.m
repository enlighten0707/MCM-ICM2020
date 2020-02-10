syms a b;
c = [a b]';

% Import initial statistics.
A = [20,30,38,45,55,77,92,129,144];
n = length(A);

%Constructing Data Matrices
for i = 2:n
    H(i) = A(i) - A(i - 1);
end
H(1) = [];

for i = 2:n
    C(i) = (A(i) + A(i-1))/2;
end
C(1) = [];

D = [-C; C.^2];
Y = H; Y = Y';

% Using the least square method to compute the parameters.
c = inv(D*D')*D*Y;
c = c';
a = c(1); b = c(2);

% Make Predictions
F = []; F(1) = A(1);
for i = 2:(n+14)
    F(i) = (a*A(1))/(b*A(1)+(a - b*A(1))*exp(a*(i-1)));
end

disp('Predictions:');
F

% Plot the data points and the fitted curve.
t1 = 0:n-1; 
t2 = 0:n+13;
figure(1);
plot(t1, A, 'ro'); hold on;
plot(t2, F, 'b--');
xlabel('Timestamp'); ylabel('Confirmed Cases');
legend('True Value','Prediction','location','northwest');
title('Oversea Infection Prediction'); grid;