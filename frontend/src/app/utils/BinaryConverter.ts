export class BinaryConverter {
    public static base64toBlob(base64: string, dataType: string = 'image/png'): Blob {
        const byteString = atob(base64.split(',')[1]);
        const buffer = new ArrayBuffer(byteString.length);
        const array = new Uint8Array(buffer);
        for (let i = 0; i < byteString.length; i++) {
            array[i] = byteString.charCodeAt(i);
        }
        return new Blob([buffer], {type: dataType});
    }
}
