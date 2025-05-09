document.addEventListener("DOMContentLoaded", () => {
  const recordBtn = document.getElementById("record-btn");
  const status = document.getElementById("recording-status");

  let mediaRecorder;
  let recordedChunks = [];

  recordBtn.addEventListener("click", async () => {
    if (!mediaRecorder || mediaRecorder.state === "inactive") {
      // 録音開始
      recordedChunks = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) recordedChunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(recordedChunks, { type: "audio/webm" });
        const file = new File([blob], "recording.webm", { type: "audio/webm" });

        const formData = new FormData();
        formData.append("audio", file);

        // 音声データをサーバーに送信
        fetch("/transcribe_audio", {
          method: "POST",
          body: formData,
        })
        .then(response => response.json())
        .then(data => {
          // サーバーから返ってきた文字起こし結果を処理
          const japaneseText = data.japanese_text;
          const englishText = data.english_text;

          // 結果を表示
          document.getElementById("result-japanese").textContent = `あなた: ${japaneseText}`;
          document.getElementById("result-english").textContent = `AI: ${englishText}`;
        })
        .catch(err => {
          console.error("送信失敗", err);
          alert("音声の送信に失敗しました。");
        });
      };

      mediaRecorder.start();
      status.textContent = "🎙️ 録音中...もう一度クリックで停止";
      recordBtn.textContent = "⏹️ 停止";

    } else {
      // 録音停止
      mediaRecorder.stop();
      status.textContent = "⏳ 処理中...";
      recordBtn.textContent = "🎙️ 録音開始";
    }
  });
});
