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

    public static byteToBase64(byteImage: ArrayBuffer): string {
        const bytes = new Uint8Array(byteImage);
        let binary = '';
        for (let i = 0; i < bytes.byteLength; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return 'data:image/png;base64,' + btoa(binary);
    }
}
