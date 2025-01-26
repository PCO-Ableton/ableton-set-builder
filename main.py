from ableton_set_builder import AbletonSetBuilder

def main():
    # Create an instance of AbletonSetBuilder with the template XML or ALS file
    builder = AbletonSetBuilder('./templates/clickque-manuel.als')
    
    # Clear the scenes and tracks in the template file
    builder.clearScenes()
    
    # Add scenes
    builder.add_template_scene(1, "Battle Belongs", color=13, tempo=120) # 
    builder.add_template_scene(2, "Reckless love", color=13, tempo=124)
    builder.add_scene(3, "Preek", color=14, tempo=120) # lege scene
    builder.add_template_scene(4, "Jezus overwinaar", color=13, tempo=128)
    
    # Build the new Ableton Live set
    builder.build_als('./output/new-live-set.als')

    print("Ableton Live set created successfully!")

if __name__ == "__main__":
    main()