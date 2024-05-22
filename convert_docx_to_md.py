import os
from docx import Document
from PIL import Image, ImageDraw, ImageFont

# Noto Sans CJK 폰트 경로 설정
font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
font_size = 20

def convert_docx_to_images(docx_file, output_dir):
    # docx 파일 열기
    doc = Document(docx_file)

    # 페이지 나누기 기준으로 문서 내용을 나눔
    pages = []
    current_page = []

    for paragraph in doc.paragraphs:
        current_page.append(paragraph.text)
        if paragraph.text == '':  # 페이지 나누기 기준 (여기서는 단순히 빈 줄로 예시)
            pages.append(current_page)
            current_page = []

    # 남아 있는 마지막 페이지 추가
    if current_page:
        pages.append(current_page)

    # 각 페이지를 이미지로 변환 및 저장
    for i, page in enumerate(pages):
        page_text = "\n".join(page)
        
        # 이미지 생성
        img = Image.new('RGB', (800, 1000), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        
        # 기본 폰트 경로 설정
        font = ImageFont.truetype(font_path, font_size)
        
        # 텍스트를 이미지에 씀
        d.text((10, 10), page_text, font=font, fill=(0, 0, 0))
        
        # 이미지 저장
        img_path = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(docx_file))[0]}_page_{i+1}.png')
        img.save(img_path)

    return len(pages), os.path.splitext(os.path.basename(docx_file))[0]

def update_md_file(md_file, num_pages, output_dir, base_name):
    with open(md_file, 'w') as f:
        f.write(f'# {base_name}\n\n')
        f.write('## Document Pages\n')
        for i in range(num_pages):
            img_path = f'{output_dir}/{base_name}_page_{i+1}.png'.replace(" ", "%20")  # 공백을 %20으로 인코딩
            f.write(f'![Page {i+1}]({img_path})\n')

def main():
    output_dir = "output_images"
    os.makedirs(output_dir, exist_ok=True)

    for docx_file in os.listdir('.'):
        if docx_file.endswith('.docx'):
            num_pages, base_name = convert_docx_to_images(docx_file, output_dir)
            md_file = f"{base_name}.md"
            update_md_file(md_file, num_pages, output_dir, base_name)

if __name__ == "__main__":
    main()
