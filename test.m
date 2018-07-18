load janie.mat


x1 = data(1:end,1);
x2 = data(1:end,2);
x3 = data(1:end,3);

fc = 5;
fs = 33;
[bb,aa] = butter(4,fc/(fs/2), 'low');
x3 = filter(bb, aa, x3);

% fc = 13;
% fs = 33;
% [bb,aa] = butter(4,fc/(fs/2), 'low');
% x1 = filter(bb, aa, x1);
% x2 = filter(bb, aa, x2);



fc = 6;
fs = 33;
[bb,aa] = butter(4,fc/(fs/2), 'high');
y1 = (filter(bb, aa, x1));
y2 = (filter(bb, aa, x2));

% plot(x1);
% hold on
% plot(x2);
% plot(y1);

plot(y2);

% plot(x3*50);