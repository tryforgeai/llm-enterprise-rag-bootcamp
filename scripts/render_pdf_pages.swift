import AppKit
import Foundation
import PDFKit

guard CommandLine.arguments.count == 3 else {
    fputs("usage: render_pdf_pages.swift <input.pdf> <output-directory>\n", stderr)
    exit(1)
}

let inputURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outputURL = URL(fileURLWithPath: CommandLine.arguments[2], isDirectory: true)

guard let document = PDFDocument(url: inputURL) else {
    fputs("could not open PDF\n", stderr)
    exit(2)
}

try FileManager.default.createDirectory(
    at: outputURL,
    withIntermediateDirectories: true
)

print("pages \(document.pageCount)")

for index in 0..<document.pageCount {
    guard let page = document.page(at: index) else {
        continue
    }

    let bounds = page.bounds(for: .mediaBox)
    let scale: CGFloat = 1.6
    let pixelWidth = Int(bounds.width * scale)
    let pixelHeight = Int(bounds.height * scale)

    let colorSpace = CGColorSpaceCreateDeviceRGB()
    guard let cgContext = CGContext(
        data: nil,
        width: pixelWidth,
        height: pixelHeight,
        bitsPerComponent: 8,
        bytesPerRow: 0,
        space: colorSpace,
        bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue
    ) else {
        continue
    }

    cgContext.setFillColor(NSColor.white.cgColor)
    cgContext.fill(CGRect(x: 0, y: 0, width: pixelWidth, height: pixelHeight))
    cgContext.scaleBy(x: scale, y: scale)
    page.draw(with: .mediaBox, to: cgContext)

    guard let image = cgContext.makeImage() else {
        continue
    }
    let bitmap = NSBitmapImageRep(cgImage: image)
    guard let png = bitmap.representation(using: .png, properties: [:]) else {
        continue
    }

    let fileURL = outputURL.appendingPathComponent(
        String(format: "page-%02d.png", index + 1)
    )
    try png.write(to: fileURL)
    print(fileURL.path)
}
