import re
import os
import argparse

# original regex line code
# (\s+CR2:.+\n)|(\s+dng:.+\n)|\s+photoshop:SidecarForExtension="DNG"\n|photoshop:EmbeddedXMPDigest=.+\n
# ^.*xmpMM:OriginalDocumentID.*$|^.*EmbeddedXMPdigest.*$|^.*xmpMM:DocumentID.*$|

def getOriginalSuffix(file_path):
    og_suffix = None
    re_search = 'dng:OriginalRawFileName=".+\.(.{3,4})"'
    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            if 'dng:OriginalRawFileName' in line:
                search = re.search(re_search,line)
                suffix = search.group(1)
                og_suffix = suffix
                break

    return og_suffix.upper()

def replaceDNGwithSuffix(og_suffix,file_path):
    new_lines = []
    fix_string = '(\s+' + og_suffix +':.+\n)|(\s+dng:.+\n)|\s+photoshop:SidecarForExtension="DNG"\n|photoshop:EmbeddedXMPDigest=.+\n'
    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            line_1 = re.sub('dng|DNG',og_suffix,line)
            line_2 = re.sub(fix_string,'',line_1)
            new_lines.append(line_2)

    return new_lines

def writeUpdates(new_lines,file_path):
    with open(file_path,'w') as f:
        f.writelines(new_lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert XMPs from small DNGs to work with original RAW files')
    parser.add_argument('-f', '--folder', required=True, help='Folder path that contains the XMPs')
    parser.add_argument('-s', '--subfolder', help='Filepath for video output', default=False)

    args = vars(parser.parse_args())

    folder_path = os.path.abspath(args['folder'])
    search_subfolders = args['subfolder']

    xmp_paths = []

    if search_subfolders:
        folder_search = os.walk(folder_path)
        for f_s in folder_search:
            xmp_paths.extend([os.path.join(f_s[0], x) for x in f_s[-1]])
    else:
        folder_contents = os.listdir(folder_path)
        xmp_paths.extend([os.path.join(folder_path, x) for x in folder_contents if '.xmp' in x])


    for xmp in xmp_paths:
        print('Updating ' + xmp)
        suffix = getOriginalSuffix(xmp)
        new_lines = replaceDNGwithSuffix(suffix,xmp)
        writeUpdates(new_lines,xmp)

