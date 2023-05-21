const fs = require('fs');
const path = require('path');
const stopwords = ["a", "acerca", "adeus", "agora", "ainda", "alem", "algmas", "algo", "algumas", "alguns", "ali", "além", "ambas", "ambos", "ano", "anos", "antes", "ao", "aonde", "aos", "apenas", "apoio", "apontar", "apos", "após", "aquela", "aquelas", "aquele", "aqueles", "aqui", "aquilo", "as", "assim", "através", "atrás", "até", "aí", "baixo", "bastante", "bem", "boa", "boas", "bom", "bons", "breve", "cada", "caminho", "catorze", "cedo", "cento", "certamente", "certeza", "cima", "cinco", "coisa", "com", "como", "comprido", "conhecido", "conselho", "contra", "contudo", "corrente", "cuja", "cujas", "cujo", "cujos", "custa", "cá", "da", "daquela", "daquelas", "daquele", "daqueles", "dar", "das", "de", "debaixo", "dela", "delas", "dele", "deles", "demais", "dentro", "depois", "desde", "desligado", "dessa", "dessas", "desse", "desses", "desta", "destas", "deste", "destes", "deve", "devem", "deverá", "dez", "dezanove", "dezasseis", "dezassete", "dezoito", "dia", "diante", "direita", "dispoe", "dispoem", "diversa", "diversas", "diversos", "diz", "dizem", "dizer", "do", "dois", "dos", "doze", "duas", "durante", "dá", "dão", "dúvida", "e", "ela", "elas", "ele", "eles", "em", "embora", "enquanto", "entao", "entre", "então", "era", "eram", "essa", "essas", "esse", "esses", "esta", "estado", "estamos", "estar", "estará", "estas", "estava", "estavam", "este", "esteja", "estejam", "estejamos", "estes", "esteve", "estive", "estivemos", "estiver", "estivera", "estiveram", "estiverem", "estivermos", "estivesse", "estivessem", "estiveste", "estivestes", "estivéramos", "estivéssemos", "estou", "está", "estás", "estávamos", "estão", "eu", "exemplo", "falta", "fará", "favor", "faz", "fazeis", "fazem", "fazemos", "fazer", "fazes", "fazia", "faço", "fez", "fim", "final", "foi", "fomos", "for", "fora", "foram", "forem", "forma", "formos", "fosse", "fossem", "foste", "fostes", "fui", "fôramos", "fôssemos", "geral", "grande", "grandes", "grupo", "ha", "haja", "hajam", "hajamos", "havemos", "havia", "hei", "hoje", "hora", "horas", "houve", "houvemos", "houver", "houvera", "houveram", "houverei", "houverem", "houveremos", "houveria", "houveriam", "houvermos", "houverá", "houverão", "houveríamos", "houvesse", "houvessem", "houvéramos", "houvéssemos", "há", "hão", "iniciar", "inicio", "ir", "irá", "isso", "ista", "iste", "isto", "já", "lado", "lhe", "lhes", "ligado", "local", "logo", "longe", "lugar", "lá", "maior", "maioria", "maiorias", "mais", "mal", "mas", "me", "mediante", "meio", "menor", "menos", "meses", "mesma", "mesmas", "mesmo", "mesmos", "meu", "meus", "mil", "minha", "minhas", "momento", "muito", "muitos", "máximo", "mês", "na", "nada", "nao", "naquela", "naquelas", "naquele", "naqueles", "nas", "nem", "nenhuma", "nessa", "nessas", "nesse", "nesses", "nesta", "nestas", "neste", "nestes", "no", "noite", "nome", "nos", "nossa", "nossas", "nosso", "nossos", "nova", "novas", "nove", "novo", "novos", "num", "numa", "numas", "nunca", "nuns", "não", "nível", "nós", "número", "o", "obra", "obrigada", "obrigado", "oitava", "oitavo", "oito", "onde", "ontem", "onze", "os", "ou", "outra", "outras", "outro", "outros", "para", "parece", "parte", "partir", "paucas", "pegar", "pela", "pelas", "pelo", "pelos", "perante", "perto", "pessoas", "pode", "podem", "poder", "poderá", "podia", "pois", "ponto", "pontos", "por", "porque", "porquê", "portanto", "posição", "possivelmente", "posso", "possível", "pouca", "pouco", "poucos", "povo", "primeira", "primeiras", "primeiro", "primeiros", "promeiro", "propios", "proprio", "própria", "próprias", "próprio", "próprios", "próxima", "próximas", "próximo", "próximos", "puderam", "pôde", "põe", "põem", "quais", "qual", "qualquer", "quando", "quanto", "quarta", "quarto", "quatro", "que", "quem", "quer", "quereis", "querem", "queremas", "queres", "quero", "questão", "quieto", "quinta", "quinto", "quinze", "quáis", "quê", "relação", "sabe", "sabem", "saber", "se", "segunda", "segundo", "sei", "seis", "seja", "sejam", "sejamos", "sem", "sempre", "sendo", "ser", "serei", "seremos", "seria", "seriam", "será", "serão", "seríamos", "sete", "seu", "seus", "sexta", "sexto", "sim", "sistema", "sob", "sobre", "sois", "somente", "somos", "sou", "sua", "suas", "são", "sétima", "sétimo", "só", "tal", "talvez", "tambem", "também", "tanta", "tantas", "tanto", "tarde", "te", "tem", "temos", "tempo", "tendes", "tenha", "tenham", "tenhamos", "tenho", "tens", "tentar", "tentaram", "tente", "tentei", "ter", "terceira", "terceiro", "terei", "teremos", "teria", "teriam", "terá", "terão", "teríamos", "teu", "teus", "teve", "tinha", "tinham", "tipo", "tive", "tivemos", "tiver", "tivera", "tiveram", "tiverem", "tivermos", "tivesse", "tivessem", "tiveste", "tivestes", "tivéramos", "tivéssemos", "toda", "todas", "todo", "todos", "trabalhar", "trabalho", "treze", "três", "tu", "tua", "tuas", "tudo", "tão", "tém", "têm", "tínhamos", "um", "uma", "umas", "uns", "usa", "usar", "vai", "vais", "valor", "veja", "vem", "vens", "ver", "verdade", "verdadeiro", "vez", "vezes", "viagem", "vindo", "vinte", "você", "vocês", "vos", "vossa", "vossas", "vosso", "vossos", "vários", "vão", "vêm", "vós", "zero", "à", "às", "área", "é", "éramos", "és", "último"];

// Set the directory path
const directoryPath = '../atas';

function wordFrequency(text, removeStopwords = true) {
    // Split the text into an array of words
    const words = text.split(/\s+/);

    // Create an object to store the frequency of each word
    const frequency = {};

    // Iterate over the words array and update the frequency object
    words.forEach(function (word) {

        // Convert the word to lowercase to ensure case-insensitive matching
        const lowercaseWord = word.toLowerCase();
        if (removeStopwords && stopwords.includes(lowercaseWord)) {
            return;
        }

        // If the word already exists in the frequency object, increment its count
        if (frequency[lowercaseWord]) {
            frequency[lowercaseWord]++;
        }
        // Otherwise, add it to the frequency object with a count of 1
        else {
            frequency[lowercaseWord] = 1;
        }
    });

    // Return the frequency object
    return frequency;
}




// Read all files in the directory
fs.readdir(directoryPath, function (err, files) {
    if (err) {
        console.log('Error reading directory:', err);
        return;
    }

    // Filter the files to only include text files
    const textFiles = files.filter(function (file) {
        return path.extname(file).toLowerCase() === '.txt';
    });

    // Read the contents of each text file and store them in an array
    const contents = [];
    textFiles.forEach(function (file) {
        const filePath = path.join(directoryPath, file);
        const fileContents = fs.readFileSync(filePath, 'utf8');
        contents.push(fileContents);
    });

    console.log(contents.length, "atas");
    const corpus = contents.join(' ');

    console.log("Word frequency with stop words:")
    const frequencyWithStopWords = wordFrequency(corpus, removeStopwords = false);
    //console.log(frequencyWithStopWords);
    // Convert the dictionary into an array of key-value pairs
    const freqWithStopWords = Object.entries(frequencyWithStopWords);
    // Sort the array by values in descending order
    freqWithStopWords.sort((a, b) => b[1] - a[1]);
    // Create a new dictionary from the sorted array
    //const sortedFrequency = Object.fromEntries(freqWithStopWords);
    console.log(freqWithStopWords.slice(0, 20))

    console.log("Word frequency without stop words:")
    const frequencyWithoutStopWords = wordFrequency(corpus, removeStopwords = true);
    //console.log(frequencyWithoutStopWords);
    // Convert the dictionary into an array of key-value pairs
    const freqWithoutStopWords = Object.entries(frequencyWithoutStopWords);
    // Sort the array by values in descending order
    freqWithoutStopWords.sort((a, b) => b[1] - a[1]);
    // Create a new dictionary from the sorted array
    //const sortedFrequency = Object.fromEntries(freqWithoutStopWords);
    console.log(freqWithoutStopWords.slice(0, 20))

});
