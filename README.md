### Convert `.als` file to `.xml`:
```bash
gzip -cd [set].als > [set].xml
```

### Python conversion:
```python
import xmltodict
xmltodict.parse()    # XML to dictionary
xmltodict.unparse()  # dictionary to XML
```

### XML input
```xml
<?xml version="1.0" encoding="utf-8"?>
<Ableton MajorVersion="5" MinorVersion="12.0_12049" SchemaChangeCount="7" Creator="Ableton Live 11.0" Revision="5094b92fa547974769f44cf233f1474777d9434a">
	<LiveSet>
		<Scenes>
			<Scene Id="0">
				<FollowAction>
					<FollowTime Value="4"></FollowTime>
					<IsLinked Value="true"></IsLinked>
					<LoopIterations Value="1"></LoopIterations>
					<FollowActionA Value="4"></FollowActionA>
					<FollowActionB Value="0"></FollowActionB>
					<FollowChanceA Value="100"></FollowChanceA>
					<FollowChanceB Value="0"></FollowChanceB>
					<JumpIndexA Value="1"></JumpIndexA>
					<JumpIndexB Value="1"></JumpIndexB>
					<FollowActionEnabled Value="false"></FollowActionEnabled>
				</FollowAction>
				<Name Value=""></Name>
				<Annotation Value=""></Annotation>
				<Color Value="-1"></Color>
				<Tempo Value="120"></Tempo>
				<IsTempoEnabled Value="false"></IsTempoEnabled>
				<TimeSignatureId Value="201"></TimeSignatureId>
				<IsTimeSignatureEnabled Value="false"></IsTimeSignatureEnabled>
				<LomId Value="0"></LomId>
				<ClipSlotsListWrapper LomId="0"></ClipSlotsListWrapper>
			</Scene>
		</Scenes>
	</LiveSet>
</Ableton>
```

### Converted dictionary
```json
{
  "Ableton": {
    "@MajorVersion": "5",
    "@MinorVersion": "12.0_12049",
    "@SchemaChangeCount": "7",
    "@Creator": "Ableton Live 11.0",
    "@Revision": "5094b92fa547974769f44cf233f1474777d9434a",
    "LiveSet": {
      "Scenes": {
        "Scene": [
          {
            "@Id": "0",
            "FollowAction": {
              "FollowTime": {
                "@Value": "4"
              },
              "IsLinked": {
                "@Value": "true"
              },
              "LoopIterations": {
                "@Value": "1"
              },
              "FollowActionA": {
                "@Value": "4"
              },
              "FollowActionB": {
                "@Value": "0"
              },
              "FollowChanceA": {
                "@Value": "100"
              },
              "FollowChanceB": {
                "@Value": "0"
              },
              "JumpIndexA": {
                "@Value": "1"
              },
              "JumpIndexB": {
                "@Value": "1"
              },
              "FollowActionEnabled": {
                "@Value": "false"
              }
            },
            "Name": {
              "@Value": ""
            },
            "Annotation": {
              "@Value": ""
            },
            "Color": {
              "@Value": "-1"
            },
            "Tempo": {
              "@Value": "120"
            },
            "IsTempoEnabled": {
              "@Value": "false"
            },
            "TimeSignatureId": {
              "@Value": "201"
            },
            "IsTimeSignatureEnabled": {
              "@Value": "false"
            },
            "LomId": {
              "@Value": "0"
            },
            "ClipSlotsListWrapper": {
              "@LomId": "0"
            }
          }
        ]
      }
    }
  }
}
```
