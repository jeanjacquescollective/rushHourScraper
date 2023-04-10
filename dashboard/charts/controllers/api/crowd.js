import fs from 'fs';
export const getCrowds = async (req, res, next) => {
    try {
        // get the repository
        // const interestRepository = DataSource.getRepository("crowds");
        let jsonFiles = fs.readdirSync('./public/json/');
        
        jsonFiles = jsonFiles.map(file => {
            return 'json/' + file;
        });
        console.log(jsonFiles);
        // get the interests and return them with status code 200
        // res.status(200).json(await interestRepository.find());
        res.status(200).json(jsonFiles);
    } catch (e) {
        // next(e.message);
        console.log('error',e.message);
    }
};