const express = require('express');
const router = express.Router();
const multer = require('multer');
const fs = require('fs');
const axios = require('axios');

const upload = multer({ dest: 'uploads/' });

function detectSeparator(firstLine) {
  const tabCount = (firstLine.match(/\t/g) || []).length;
  const commaCount = (firstLine.match(/,/g) || []).length;
  return tabCount > commaCount ? '\t' : ',';
}

router.post('/', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ success: false, error: 'No file uploaded' });
    }

    const fileContent = fs.readFileSync(req.file.path, 'utf8');
    const lines = fileContent.split('\n').filter(line => line.trim());
    
    const separator = detectSeparator(lines[0]);
    console.log('Detected separator:', separator === '\t' ? 'TAB' : 'COMMA');
    
    const records = [];
    for (let i = 1; i < Math.min(lines.length, 101); i++) {
      const values = lines[i].split(separator);
      if (values.length >= 6) {
        records.push({
          date: values[1],
          onpromotion: parseInt(values[5]) || 0
        });
      }
    }

    fs.unlinkSync(req.file.path);

    let predictions = [];
    let mlError = null;
    
    try {
      const mlResponse = await axios.post(
        `${process.env.ML_SERVICE_URL}/batch_predict`,
        { records: records },
        { timeout: 30000 }
      );
      
      if (mlResponse.data.success) {
        predictions = mlResponse.data.predictions || [];
      } else {
        mlError = mlResponse.data.error || 'ML service returned error';
      }
    } catch (error) {
      mlError = error.message;
      console.log('ML service error:', error.message);
    }

    res.json({
      success: true,
      total_rows: lines.length - 1,
      processed_rows: records.length,
      predictions: predictions.slice(0, 5),
      predictions_count: predictions.length,
      ml_error: mlError,
      sample: records.slice(0, 3)
    });

  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;
