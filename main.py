import httpx
import json
import time
from parse_json import parse

# Первый запрос для получения заголовков и кук
def get_initial_headers_and_cookies():
    url = "https://x.com/elonmusk/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    
    with httpx.Client() as client:
        response = client.get(url, headers=headers)
        print(response.raise_for_status())
        
        # Получаем куки
        cookies = response.cookies
        
        # Сохраняем заголовки
        headers.update({
            "Accept": "application/json",
            "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",  # Замените на ваш токен
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        })
        return headers, cookies

# Второй запрос к API с использованием сохраненных заголовков и кук
def fetch_and_save_json(url, file_path, headers, cookies):
    time.sleep(2)
    with httpx.Client() as client:
        while True:
            try:
                response = client.get(url, headers=headers,cookies=cookies)
                response.raise_for_status()
                return response.json()  # Успешный ответ, возвращаем JSON
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Обработка ошибки 429
                    reset_time = int(e.response.headers.get("X-Rate-Limit-Reset", time.time() + 60))
                    wait_time = reset_time - int(time.time())
                    print(f"Превышен лимит запросов, ожидаем {wait_time} секунд...")
                    time.sleep(wait_time)  # Ожидание сброса лимита
                else:
                    print(f"Ошибка HTTP: {e}")
                    break
            except httpx.RequestError as e:
                print(f"Ошибка запроса: {e}")
                break
        
            data = response.json()
        
        # Сохраняем JSON в файл
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"JSON сохранен в файл: {file_path}")

# Главная функция
def main():
    url_api = r"https://api.x.com/graphql/E3opETHurmVJflFsUBVuUQ/UserTweets?variables=%7B%22userId%22%3A%2244196397%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticlePlainText%22%3Afalse%7D"
    file_path = "response.json"
    
    # Получаем заголовки и куки с первой страницы
    headers, cookies = get_initial_headers_and_cookies()
    
    # Делаем запрос к API
    fetch_and_save_json(url_api, file_path, headers, cookies)

# Запускаем программу
if __name__ == "__main__":
    main()
    time.sleep(2)
    parse()
