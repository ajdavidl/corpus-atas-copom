listFiles = dir('../atas');
corpus = "";
for i = 3:length(listFiles)
    str = fileread([listFiles(i).folder '\' listFiles(i).name]);
    corpus = strcat(corpus, ' ', str); %#ok<AGROW>
end

Mystopwords = {'de','a','em','e','o','do','da','no','para','que','com','se', ...
    'os','as','dos','na','ao','das','p','1','por','pelo','relação','mês',...
    'nas','sobre','pela','até','à','nos','um','como','não','entre','mesmo', ...
    'seu','seus','sua','suas','é','está','às','aos','10','após','também',...
    'esse','esses','essa','essas','isso','este','estes','esta','estas','isto',...
    '0%','1%','2%','3%','4%','5%','6%','7%','8%','9%','uma','desde',...
    '0','1','2','3','4','5','6','7','8','9'};
NRWORDS=20;

disp('WORD FREQUENCY WITH STOP WORDS')
[result, count] = wordFrequency(corpus, NRWORDS, {});
disp('')
disp('WORD FREQUENCY WITHOUT STOP WORDS')
[result2, count2] = wordFrequency(corpus, NRWORDS, Mystopwords);

function [result,count] = wordFrequency(text, nrWords, stopwords)
% Adapted from:
% https://rosettacode.org/wiki/Word_frequency#MATLAB_/_Octave
    WITHSTOPWORDS = boolean(length(stopwords));
    DELIMITER={' ', ',', ';', ':', '.', '/', '*', '!', '?', '<', '>', '(', ')', '[', ']','{', '}', '&','$','§','"','”','“','-','—','‘','\t','\n','\r'};
    words  = sort(strsplit(lower(text),DELIMITER));
    flag   = [find(~strcmp(words(1:end-1),words(2:end))),length(words)];
    dwords = words(flag);   % get distinct words, and ...
    count  = diff([0,flag]);  % ... the corresponding occurance frequency
    [~,idx] = sort(-count);       % sort according to occurance
    result = dwords(idx);
    count  = count(idx);
    c = 1;
    k = 1;
    while c <= nrWords && k < length(result)
        if WITHSTOPWORDS
        indx = find(strcmp(stopwords, result{k}), 1);
        if isempty(indx)
            fprintf(1,'%d\t%s\n',count(k),result{k})
            c = c + 1;
        end
        k = k + 1;
        else
            fprintf(1,'%d\t%s\n',count(k),result{k})
            c = c + 1;
            k = k + 1;
        end
    end
end
 