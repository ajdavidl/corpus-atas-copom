listFiles = dir('../atas');
corpus = "";
for i = 3:length(listFiles)
    str = fileread([listFiles(i).folder '/' listFiles(i).name]);
    corpus = strcat(corpus, ' ', str); %#ok<AGROW>
end
 
corpus = char(corpus);
A = letter_frequency(corpus);
 
function A = letter_frequency(t)
% Adapted from https://rosettacode.org/wiki/Letter_frequency?section=15#MATLAB_/_Octave
    if ischar(t)
        t = abs(t);
    end
    A = sparse(t+1,1,1);
    A = full(A);
    fprintf('"%c" : %i\n',[find(A)-1,A(A>0)]')
end