import express from 'express';
import cors from 'cors';
import { exec } from 'child_process';

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors()); 

app.get('/download', async (req, res) => {
  const videoUrl = req.query.url;

  if (!videoUrl) {
    return res.status(400).send('No URL provided');
  }

  try {
    res.header('Content-Disposition', 'attachment; filename="video.mp4"');
    res.header('Content-Type', 'video/mp4');

    // Full path to yt-dlp.exe on your Desktop
    const ytDlpPath = "C:\\Users\\DELL\\Desktop\\yt-dlp.exe";
    const downloadProcess = exec(`"${ytDlpPath}" -o - ${videoUrl}`);

    downloadProcess.stdout.pipe(res);

    downloadProcess.on('error', (error) => {
      console.error('Error downloading video:', error);
      res.status(500).send('Failed to download the video');
    });
  } catch (error) {
    console.error('Error downloading video:', error);
    res.status(500).send('Failed to download the video');
  }
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
