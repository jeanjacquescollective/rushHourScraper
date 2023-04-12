import * as path from 'path';

export const fetchCrowd = async (req, res, next) => {
  const query = req.query.query;
  res.sendFile(path.join(path.resolve(path.dirname('')), 'public/index.html'));
}
