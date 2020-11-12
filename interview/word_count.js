const fs = require("fs");


function word_count(filename) {
    let result = {};

    fs.readFile(filename, {encoding: 'utf-8'}, function(err, data){
    if (!err) {

        data.split('\n').forEach(
            line => line.split(' ').forEach(
                word => {
                   if (word in result) {
                       result[word] += 1
                   } else {
                       result[word] = 1
                   }
                }
            )
        );

        result = Object.entries(result).sort(
            (a, b) => {
                if (a[1] < b[1]) return 1;
                if (a[1] > b[1]) return -1;
                if (a[0].localeCompare(b[0]) === 1) return 1;
                if (b[0].localeCompare(a[0]) === -1) return -1;
            }
        );

        result.forEach(
            word => console.log(`<${word[0]}>: <${word[1]}>`)
        )
    } else {
        console.log(`File with ${filename} does not exist`);
    }
  });
}


function main() {

  let filename = process.argv.slice(2)[0];
  console.log(filename);

  word_count(filename);
}


main();
