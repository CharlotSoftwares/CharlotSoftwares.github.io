async function decodeJPXPImage(imgElement) {
  const url = imgElement.src;
  const response = await fetch(url);
  const buffer = await response.arrayBuffer();
  const data = new DataView(buffer);

  const magic = new TextDecoder().decode(new Uint8Array(buffer.slice(0, 4)));
  if (magic !== "JPX+") throw new Error("Invalid JPXP format");

  const metaLength = data.getUint32(16, true);
  const metaEnd = 20 + metaLength;
  const imageLength = data.getUint32(metaEnd, true);
  const imageStart = metaEnd + 4;
  const imageEnd = imageStart + imageLength;
  const avifBlob = new Blob([buffer.slice(imageStart, imageEnd)], { type: "image/avif" });
  const avifURL = URL.createObjectURL(avifBlob);

  imgElement.src = avifURL; // Replace src with AVIF blob
}

const img = document.getElementById("jpxpImage");
decodeJPXPImage(img).catch(console.error);
