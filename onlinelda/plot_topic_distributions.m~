function plot_topic_distributions()
    gamma=load('parameters/gamma-all.dat');
    indices = sort(round((rand(1,12).*814)+1));
    figure
    for i = 1:12
        subplot(3,4,i)
        plot(gamma(indices(i),:)./sum(gamma(indices(i),:)))
        title(cstrcat("Operation ", num2str(indices(i))))
    end
endfunction
