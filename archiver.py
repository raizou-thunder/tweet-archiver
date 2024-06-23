import time
import json
import requests

username = 'raizou_thunder'

token = ''
cstf_token = ''
auth_token = ''
transaction_id = ''

headers = {
    'accept': '*/*',
    'accept-language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': token,
    'content-type': 'application/json',
    'cookie': f'auth_token={auth_token}; ct0={cstf_token};',
    'sec-ch-ua': '\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-client-transaction-id': transaction_id,
    'x-csrf-token': cstf_token,
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'ja'
}

tweet_data = {}

response = requests.get(f'https://twitter.com/i/api/graphql/k5XapwcSikNsEsILW5FvgA/UserByScreenName?variables={{"screen_name":"{username}","withSafetyModeUserFields":true}}&features={{"hidden_profile_likes_enabled":true,"hidden_profile_subscriptions_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}}&fieldToggles={{"withAuxiliaryUserLabels":false}}', headers=headers)
if response.status_code == 200:
    userdata = response.json()['data']['user']['result']

    response = requests.get(f'https://twitter.com/i/api/graphql/LJwZwXzqk7wHyXPa3SQt4Q/UserTweets?variables={{"userId":"{userdata["rest_id"]}","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}}&features={{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}}', headers=headers)
    print('\n\n', response.status_code, response.text)
    if response.status_code == 200:
        cursor = ''
        tweet_data = response.json()
        tweet_data['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'] = []
        for instruction in response.json()['data']['user']['result']['timeline_v2']['timeline']['instructions']:
            if instruction['type'] == 'TimelineAddEntries':
                for entry in instruction['entries']:
                    if entry['entryId'].startswith('tweet-'):
                        tweet_data['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'].append(entry)
                    elif entry['entryId'].startswith('cursor-bottom-'):
                        cursor = entry['content']['value']
        while True:
            time.sleep(10)
            response = requests.get(f'https://twitter.com/i/api/graphql/LJwZwXzqk7wHyXPa3SQt4Q/UserTweets?variables={{"userId":"{userdata["rest_id"]}","count":20,"cursor":"{cursor}","includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}}&features={{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}}', headers=headers)
            print('\n\n', response.status_code, response.text)
            if len(response.json()['data']['user']['result']['timeline_v2']['timeline']['instructions'][0]['entries']) <= 2:
                break
            if response.status_code == 200:
                for instruction in response.json()['data']['user']['result']['timeline_v2']['timeline']['instructions']:
                    if instruction['type'] == 'TimelineAddEntries':
                        for entry in instruction['entries']:
                            if entry['entryId'].startswith('tweet-'):
                                tweet_data['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'].append(entry)
                            elif entry['entryId'].startswith('cursor-bottom-'):
                                cursor = entry['content']['value']

    with open('./tweets.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(tweet_data))