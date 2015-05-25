# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import country_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_country_company'),
        #('main', '0009_more_rosters'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='address_line_1',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='address_line_2',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='city',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='country',
            field=country_utils.fields.CountryField(blank=True, max_length=2, null=True, choices=[(b'AD', 'Andorra'), (b'AE', 'United Arab Emirates'), (b'AF', 'Afghanistan'), (b'AG', 'Antigua and Barbuda'), (b'AI', 'Anguilla'), (b'AL', 'Albania'), (b'AM', 'Armenia'), (b'AN', 'Netherlands Antilles'), (b'AO', 'Angola'), (b'AQ', 'Antarctica'), (b'AR', 'Argentina'), (b'AS', 'American Samoa'), (b'AT', 'Austria'), (b'AU', 'Australia'), (b'AW', 'Aruba'), (b'AX', '\xc5land Islands'), (b'AZ', 'Azerbaijan'), (b'BA', 'Bosnia and Herzegovina'), (b'BB', 'Barbados'), (b'BD', 'Bangladesh'), (b'BE', 'Belgium'), (b'BF', 'Burkina Faso'), (b'BG', 'Bulgaria'), (b'BH', 'Bahrain'), (b'BI', 'Burundi'), (b'BJ', 'Benin'), (b'BL', 'Saint Barth\xe9lemy'), (b'BM', 'Bermuda'), (b'BN', 'Brunei Darussalam'), (b'BO', 'Bolivia, Plurinational State of'), (b'BR', 'Brazil'), (b'BS', 'Bahamas'), (b'BT', 'Bhutan'), (b'BV', 'Bouvet Island'), (b'BW', 'Botswana'), (b'BY', 'Belarus'), (b'BZ', 'Belize'), (b'CA', 'Canada'), (b'CC', 'Cocos (Keeling) Islands'), (b'CD', 'Congo, the Democratic Republic of the'), (b'CF', 'Central African Republic'), (b'CG', 'Congo'), (b'CH', 'Switzerland'), (b'CI', "C\xf4te d'Ivoire"), (b'CK', 'Cook Islands'), (b'CL', 'Chile'), (b'CM', 'Cameroon'), (b'CN', 'China'), (b'CO', 'Colombia'), (b'CR', 'Costa Rica'), (b'CU', 'Cuba'), (b'CV', 'Cape Verde'), (b'CX', 'Christmas Island'), (b'CY', 'Cyprus'), (b'CZ', 'Czech Republic'), (b'DE', 'Germany'), (b'DJ', 'Djibouti'), (b'DK', 'Denmark'), (b'DM', 'Dominica'), (b'DO', 'Dominican Republic'), (b'DZ', 'Algeria'), (b'EC', 'Ecuador'), (b'EE', 'Estonia'), (b'EG', 'Egypt'), (b'EH', 'Western Sahara'), (b'ER', 'Eritrea'), (b'ES', 'Spain'), (b'ET', 'Ethiopia'), (b'FI', 'Finland'), (b'FJ', 'Fiji'), (b'FK', 'Falkland Islands (Malvinas)'), (b'FM', 'Micronesia, Federated States of'), (b'FO', 'Faroe Islands'), (b'FR', 'France'), (b'GA', 'Gabon'), (b'GB', 'United Kingdom'), (b'GD', 'Grenada'), (b'GE', 'Georgia'), (b'GF', 'French Guiana'), (b'GG', 'Guernsey'), (b'GH', 'Ghana'), (b'GI', 'Gibraltar'), (b'GL', 'Greenland'), (b'GM', 'Gambia'), (b'GN', 'Guinea'), (b'GP', 'Guadeloupe'), (b'GQ', 'Equatorial Guinea'), (b'GR', 'Greece'), (b'GS', 'South Georgia and the South Sandwich Islands'), (b'GT', 'Guatemala'), (b'GU', 'Guam'), (b'GW', 'Guinea-Bissau'), (b'GY', 'Guyana'), (b'HK', 'Hong Kong'), (b'HM', 'Heard Island and McDonald Islands'), (b'HN', 'Honduras'), (b'HR', 'Croatia'), (b'HT', 'Haiti'), (b'HU', 'Hungary'), (b'ID', 'Indonesia'), (b'IE', 'Ireland'), (b'IL', 'Israel'), (b'IM', 'Isle of Man'), (b'IN', 'India'), (b'IO', 'British Indian Ocean Territory'), (b'IQ', 'Iraq'), (b'IR', 'Iran, Islamic Republic of'), (b'IS', 'Iceland'), (b'IT', 'Italy'), (b'JE', 'Jersey'), (b'JM', 'Jamaica'), (b'JO', 'Jordan'), (b'JP', 'Japan'), (b'KE', 'Kenya'), (b'KG', 'Kyrgyzstan'), (b'KH', 'Cambodia'), (b'KI', 'Kiribati'), (b'KM', 'Comoros'), (b'KN', 'Saint Kitts and Nevis'), (b'KP', "Korea, Democratic People's Republic of"), (b'KR', 'Korea, Republic of'), (b'KW', 'Kuwait'), (b'KY', 'Cayman Islands'), (b'KZ', 'Kazakhstan'), (b'LA', "Lao People's Democratic Republic"), (b'LB', 'Lebanon'), (b'LC', 'Saint Lucia'), (b'LI', 'Liechtenstein'), (b'LK', 'Sri Lanka'), (b'LR', 'Liberia'), (b'LS', 'Lesotho'), (b'LT', 'Lithuania'), (b'LU', 'Luxembourg'), (b'LV', 'Latvia'), (b'LY', 'Libyan Arab Jamahiriya'), (b'MA', 'Morocco'), (b'MC', 'Monaco'), (b'MD', 'Moldova, Republic of'), (b'ME', 'Montenegro'), (b'MF', 'Saint Martin (French part)'), (b'MG', 'Madagascar'), (b'MH', 'Marshall Islands'), (b'MK', 'Macedonia, the former Yugoslav Republic of'), (b'ML', 'Mali'), (b'MM', 'Myanmar'), (b'MN', 'Mongolia'), (b'MO', 'Macao'), (b'MP', 'Northern Mariana Islands'), (b'MQ', 'Martinique'), (b'MR', 'Mauritania'), (b'MS', 'Montserrat'), (b'MT', 'Malta'), (b'MU', 'Mauritius'), (b'MV', 'Maldives'), (b'MW', 'Malawi'), (b'MX', 'Mexico'), (b'MY', 'Malaysia'), (b'MZ', 'Mozambique'), (b'NA', 'Namibia'), (b'NC', 'New Caledonia'), (b'NE', 'Niger'), (b'NF', 'Norfolk Island'), (b'NG', 'Nigeria'), (b'NI', 'Nicaragua'), (b'NL', 'Netherlands'), (b'NO', 'Norway'), (b'NP', 'Nepal'), (b'NR', 'Nauru'), (b'NU', 'Niue'), (b'NZ', 'New Zealand'), (b'OM', 'Oman'), (b'PA', 'Panama'), (b'PE', 'Peru'), (b'PF', 'French Polynesia'), (b'PG', 'Papua New Guinea'), (b'PH', 'Philippines'), (b'PK', 'Pakistan'), (b'PL', 'Poland'), (b'PM', 'Saint Pierre and Miquelon'), (b'PN', 'Pitcairn'), (b'PR', 'Puerto Rico'), (b'PS', 'Palestinian Territory, Occupied'), (b'PT', 'Portugal'), (b'PW', 'Palau'), (b'PY', 'Paraguay'), (b'QA', 'Qatar'), (b'RE', 'R\xe9union'), (b'RO', 'Romania'), (b'RS', 'Serbia'), (b'RU', 'Russian Federation'), (b'RW', 'Rwanda'), (b'SA', 'Saudi Arabia'), (b'SB', 'Solomon Islands'), (b'SC', 'Seychelles'), (b'SD', 'Sudan'), (b'SE', 'Sweden'), (b'SG', 'Singapore'), (b'SH', 'Saint Helena'), (b'SI', 'Slovenia'), (b'SJ', 'Svalbard and Jan Mayen'), (b'SK', 'Slovakia'), (b'SL', 'Sierra Leone'), (b'SM', 'San Marino'), (b'SN', 'Senegal'), (b'SO', 'Somalia'), (b'SR', 'Suriname'), (b'ST', 'Sao Tome and Principe'), (b'SV', 'El Salvador'), (b'SY', 'Syrian Arab Republic'), (b'SZ', 'Swaziland'), (b'TC', 'Turks and Caicos Islands'), (b'TD', 'Chad'), (b'TF', 'French Southern Territories'), (b'TG', 'Togo'), (b'TH', 'Thailand'), (b'TJ', 'Tajikistan'), (b'TK', 'Tokelau'), (b'TL', 'Timor-Leste'), (b'TM', 'Turkmenistan'), (b'TN', 'Tunisia'), (b'TO', 'Tonga'), (b'TR', 'Turkey'), (b'TT', 'Trinidad and Tobago'), (b'TV', 'Tuvalu'), (b'TW', 'Taiwan, Province of China'), (b'TZ', 'Tanzania, United Republic of'), (b'UA', 'Ukraine'), (b'UG', 'Uganda'), (b'UM', 'United States Minor Outlying Islands'), (b'US', 'United States'), (b'UY', 'Uruguay'), (b'UZ', 'Uzbekistan'), (b'VA', 'Holy See (Vatican City State)'), (b'VC', 'Saint Vincent and the Grenadines'), (b'VE', 'Venezuela, Bolivarian Republic of'), (b'VG', 'Virgin Islands, British'), (b'VI', 'Virgin Islands, U.S.'), (b'VN', 'Viet Nam'), (b'VU', 'Vanuatu'), (b'WF', 'Wallis and Futuna'), (b'WS', 'Samoa'), (b'YE', 'Yemen'), (b'YT', 'Mayotte'), (b'ZA', 'South Africa'), (b'ZM', 'Zambia'), (b'ZW', 'Zimbabwe')]),
            preserve_default=True,
        ),
    ]
