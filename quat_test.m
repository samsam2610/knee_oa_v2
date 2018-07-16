load quat_test.mat

[r, c, v] = quat2angle(data, 'XYX');
r = rad2deg(r);
c = rad2deg(c);
v = rad2deg(v);
%xyx
subplot(1,3,1);
plot(r);
subplot(1,3,2);
plot(c);
subplot(1,3,3);
plot(v);