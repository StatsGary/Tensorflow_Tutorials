# Bing download
from bing_image_downloader import downloader
query_str = 'lewis grabban'
output_dir = 'images'
downloader.download(query_str, limit=100,  output_dir=output_dir, 
                    adult_filter_off=True, force_replace=False, 
                    timeout=60, verbose=True)