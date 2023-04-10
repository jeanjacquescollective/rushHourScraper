import * as path from 'path';
import * as fs from 'fs';
export default {
    home: (req, res) => {     
        res.sendFile(path.join(path.resolve(path.dirname('')), 'public/index.html'));
    },
    second: (req, res) => {
        res.send('This is the second page');
    },
};