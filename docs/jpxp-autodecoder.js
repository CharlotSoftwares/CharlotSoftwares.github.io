async function decodeJPXPImage(imgElement, url) {
  try {
    const response = await fetch(url);
    const buffer = await response.arrayBuffer();
    const data = new DataView(buffer);

    // Validate JPXP magic
    const magic = new TextDecoder().decode(new Uint8Array(buffer.slice(0, 4)));
    if (magic !== "JPX+") throw new Error("Not a JPXP file");

    const metaLength = data.getUint32(16, true);
    const metaEnd = 20 + metaLength;
    const imageLength = data.getUint32(metaEnd, true);
    const imageStart = metaEnd + 4;
    const imageEnd = imageStart + imageLength;

    const avifBlob = new Blob([buffer.slice(imageStart, imageEnd)], { type: "image/avif" });
    const avifURL = URL.createObjectURL(avifBlob);
    imgElement.src = avifURL;
  } catch (err) {
    console.error(`Failed to decode JPXP: ${url}`, err);
    imgElement.alt = "JPXP decode failed";
  }
}

function autoDecodeAllJPXP() {
  const jpxpImages = document.querySelectorAll('img[src$=".jpxp"]');
  jpxpImages.forEach(img => {
    const url = img.getAttribute("src");
    decodeJPXPImage(img, url);
  });
}

window.addEventListener("DOMContentLoaded", autoDecodeAllJPXP);
