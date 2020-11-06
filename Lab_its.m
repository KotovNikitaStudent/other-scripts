% Работу выполнил студент группы ИТС-11МО Иванов ИИ
clc;
clear;
B = 0.4;
K = 1e6;
R = raylrnd(B, [1 K]);
N = length(R);
b = ceil(5*log10(N)); 
figure;
H = histogram(R,b,'Normalization','pdf');
x = 0:0.01:2.37;
pd = makedist('Rayleigh','b',B);
f = pdf(pd, x);
hold on;
plot(x, H, x, f, 'Color', 'r');
title('Распределение Рэлея', 'FontSize',20);
xlabel('x', 'FontSize',16);
ylabel('Pтеор(x),Pэмп(x)', 'FontSize',16);
legend({'Эмпирическое распределение', 'Теоретическое распределение'}, ...
    'FontSize',12)
grid on;
M_emp = nanmean(R);
Var_emp = var(R);
M_teor = sqrt(pi/2)*B;
Var_teor = (2-(pi/2))*B^2;
ph = mle(R, 'distribution', 'Rayleigh');

be = H.BinEdges;
bc = H.BinCounts;
bo = bc./N;
Hi_square = 0;
for i=1:b-1
    Hi_square = Hi_square + ((bc(i) - N.*(cdf('Rayleigh',be(i+1),ph)-cdf('Rayleigh',be(i),ph))).^2)...
        /(N.*(cdf('Rayleigh',be(i+1),ph)-cdf('Rayleigh',be(i),ph)));
end
disp("Генерация выборки с параметром распределения: " + B);
disp("Количество значений в выборке: " + K);
disp("Среднее значение эмпирическое: "  + M_emp);
disp("Среднее значение теоретическое: "  + M_teor);
disp("Дисперсия эмпирическое: "  + Var_emp);
disp("Дисперсия теоретическое: "  + Var_teor);
disp("Критерий хи-квадрат: "  + Hi_square);





